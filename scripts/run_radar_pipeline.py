"""
End-to-End Radar Signal Processing, EDA, and Dual-Phase Detection Demonstration
Executes:
  1. High-Fidelity FMCW I/Q Simulation (Multi-target + Clutter + Noise)
  2. Primitive DSP (Range FFT, MTI, Doppler FFT, 2D CA/OS-CFAR, MUSIC AoA, DBSCAN)
  3. AI / Deep Learning Range-Doppler Detection Training & Inference
  4. Publication-Grade Multi-Panel Visualization & Export
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import torch

# Add workspace to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sim.radar_config import RadarConfig
from src.sim.target import RadarTarget, create_standard_traffic_scenario
from src.sim.radar_sim import FMCWRadarSimulator
from src.dsp.range_processing import RangeProcessor
from src.dsp.clutter_removal import ClutterFilter
from src.dsp.doppler_processing import DopplerProcessor
from src.dsp.cfar_detector import CFARDetector2D
from src.dsp.aoa_estimation import AngleEstimator
from src.dsp.clustering import RadarClusterer
from src.dsp.radar_pipeline import ClassicalRadarPipeline
from src.models.radar_dataset import RadarDataset
from src.models.radar_detector_cnn import RadarObjectDetectorCNN
from src.models.train_detector import train_radar_detector

def run_full_pipeline():
    print("=" * 80)
    print("      FMCW RADAR SIGNAL PROCESSING & AI DETECTION TESTBENCH (2026)")
    print("=" * 80)

    # 1. System Parameters
    cfg = RadarConfig(
        fc=77e9,              # 77 GHz
        bandwidth=1.0e9,      # 1 GHz sweep (Range resolution: 0.15 m)
        chirp_duration=50e-6, # 50 us
        num_samples=256,
        num_chirps=128,
        num_rx=4,
        sampling_rate=5.12e6
    )

    print(f"[+] Carrier Frequency (fc): {cfg.fc / 1e9:.1f} GHz | Wavelength: {cfg.wavelength * 1e3:.2f} mm")
    print(f"[+] Bandwidth: {cfg.bandwidth / 1e9:.2f} GHz | Range Resolution: {cfg.range_resolution:.3f} m")
    print(f"[+] Max Range: {cfg.max_unambiguous_range:.2f} m | Max Velocity: {cfg.max_unambiguous_velocity:.2f} m/s")
    print(f"[+] Velocity Resolution: {cfg.velocity_resolution:.3f} m/s")

    # 2. Scene Definition
    targets = create_standard_traffic_scenario()
    print(f"\n[+] Active Multi-Target Scene ({len(targets)} targets):")
    for i, t in enumerate(targets):
        print(f"    - Target #{i+1} [{t.label.upper()}]: Range={t.range_m:.1f}m, Velocity={t.velocity_mps:+.1f}m/s, Azimuth={t.azimuth_deg:+.1f} deg, RCS={t.rcs_dbsm:+.1f}dBsm")

    # 3. Simulate Raw I/Q ADC Signals
    print("\n[+] Synthesizing Raw 3D Radar Cube (Rx x Chirps x Samples) with Clutter and Noise...")
    sim = FMCWRadarSimulator(cfg)
    radar_cube = sim.generate_radar_cube(
        targets=targets,
        snr_db=18.0,
        clutter_ratio_db=10.0,
        include_clutter=True,
        seed=42
    )
    print(f"    Radar Cube Shape: {radar_cube.shape} | Data Type: {radar_cube.dtype}")

    # 4. Classical DSP Pipeline Execution
    print("\n[+] Executing Classical DSP Processing Chain...")
    pipeline = ClassicalRadarPipeline(config=cfg, cfar_type="ca", p_fa=1e-4, clutter_method="mean_subtraction")
    dsp_results = pipeline.process_radar_cube(radar_cube)

    print(f"    - Clutter Attenuation (CA): {dsp_results['clutter_attenuation_db']:.2f} dB")
    print(f"    - 2D CFAR Detections Found: {len(dsp_results['raw_detections'])} peaks")
    print(f"    - Clustered Objects Extracted: {len(dsp_results['detected_objects'])} entities")

    print("\n--- DSP Target Estimation vs. Ground Truth ---")
    for obj in dsp_results["detected_objects"]:
        print(f"    [*] Detected Object #{obj['object_id']}: Range = {obj['range_m']:.2f} m, Velocity = {obj['velocity_mps']:+.2f} m/s, Azimuth = {obj['azimuth_deg']:+.1f} deg, Points = {obj['num_points']}")

    # 5. AoA High-Resolution MUSIC Spectrum on Target Range Bins
    aoa_estimator = pipeline.aoa_estimator
    rdm = dsp_results["rdm"]
    angles_deg, music_spec_1, est_angle_1 = aoa_estimator.estimate_aoa_music(
        rdm[:, dsp_results["raw_detections"][0]["doppler_bin"], dsp_results["raw_detections"][0]["range_bin"]]
    )
    _, capon_spec_1, _ = aoa_estimator.estimate_aoa_capon(
        rdm[:, dsp_results["raw_detections"][0]["doppler_bin"], dsp_results["raw_detections"][0]["range_bin"]]
    )

    # 6. Micro-Doppler Signature for Pedestrian
    print("\n[+] Computing Micro-Doppler STFT Spectrogram for dynamic pedestrian...")
    ped_target = [t for t in targets if t.label == "pedestrian"][0]
    # Long continuous slow-time signal
    t_extended = np.linspace(0, 1.0, 512)
    ped_slow_time = np.exp(1j * 2 * np.pi * (2 * ped_target.velocity_mps / cfg.wavelength) * t_extended)
    if ped_target.micro_doppler_freq and ped_target.micro_doppler_amp:
        ped_slow_time *= np.exp(1j * (4 * np.pi / cfg.wavelength) * (ped_target.micro_doppler_amp / (2*np.pi*ped_target.micro_doppler_freq)) * np.sin(2 * np.pi * ped_target.micro_doppler_freq * t_extended))
    ped_slow_time += 0.2 * (np.random.randn(len(t_extended)) + 1j * np.random.randn(len(t_extended)))
    md_freqs, md_times, md_spec = DopplerProcessor.compute_micro_doppler_spectrogram(ped_slow_time, fs=512.0)

    # 7. Phase 2: Train Deep Learning Radar CNN Detector
    print("\n[+] Phase 2: Training PyTorch Radar Object Detector CNN on synthetic Range-Doppler heatmaps...")
    model, history = train_radar_detector(num_samples=80, epochs=4, batch_size=8, lr=1e-3)

    # Model inference on test frame
    model.eval()
    rdm_power = dsp_results["rdm_power_db"]
    rdm_norm = (rdm_power - np.min(rdm_power)) / (np.max(rdm_power) - np.min(rdm_power) + 1e-8)
    test_tensor = torch.tensor(rdm_norm, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        cls_logits, box_preds = model(test_tensor)
        cls_probs = torch.sigmoid(cls_logits).squeeze(0).numpy() # (num_classes, H, W)
        car_heatmap = cls_probs[1]
        ped_heatmap = cls_probs[2]

    # 8. Render Multi-Panel Publication-Grade EDA Dashboard
    print("\n[+] Rendering Comprehensive Radar EDA and Evaluation Visualizations...")
    fig = plt.figure(figsize=(20, 14), dpi=150)
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

    range_axis = dsp_results["range_axis"]
    velocity_axis = dsp_results["velocity_axis"]

    # Panel 1: Time Domain ADC I/Q Chirp
    ax1 = fig.add_subplot(gs[0, 0])
    sample_idx = np.arange(cfg.num_samples)
    ax1.plot(sample_idx[:128], np.real(radar_cube[0, 0, :128]), label="In-Phase (I)", color="#1f77b4", lw=1.5)
    ax1.plot(sample_idx[:128], np.imag(radar_cube[0, 0, :128]), label="Quadrature (Q)", color="#ff7f0e", lw=1.5, alpha=0.8)
    ax1.set_title("1. Raw ADC Dechirped I/Q Signal (Chirp #0)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Fast-Time Sample Index (n)")
    ax1.set_ylabel("Voltage Amplitude (V)")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", fontsize=8)

    # Panel 2: 1D Range Profile (Raw vs MTI Filtered)
    ax2 = fig.add_subplot(gs[0, 1])
    raw_range_pwr = 10 * np.log10(np.mean(np.abs(dsp_results["range_cube"][0])**2, axis=0))
    filt_range_pwr = 10 * np.log10(np.mean(np.abs(dsp_results["filtered_range_cube"][0])**2, axis=0))
    ax2.plot(range_axis, raw_range_pwr, label="Raw (with Clutter)", color="#d62728", lw=1.5, alpha=0.7)
    ax2.plot(range_axis, filt_range_pwr, label="MTI Cleaned", color="#2ca02c", lw=1.8)
    ax2.set_title(f"2. 1D Range Profile (MTI Clutter Attenuation: {dsp_results['clutter_attenuation_db']:.1f} dB)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Range (meters)")
    ax2.set_ylabel("Power (dB)")
    ax2.set_xlim([0, 40])
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right", fontsize=8)

    # Panel 3: 2D Range-Doppler Heatmap
    ax3 = fig.add_subplot(gs[0, 2])
    extent = [range_axis[0], range_axis[-1], velocity_axis[0], velocity_axis[-1]]
    im3 = ax3.imshow(
        dsp_results["rdm_power_db"],
        aspect="auto",
        origin="lower",
        extent=extent,
        cmap="jet",
        vmin=np.percentile(dsp_results["rdm_power_db"], 10),
        vmax=np.max(dsp_results["rdm_power_db"])
    )
    ax3.set_title("3. 2D Range-Doppler Matrix (RDM)", fontsize=11, fontweight="bold")
    ax3.set_xlabel("Range (m)")
    ax3.set_ylabel("Radial Velocity (m/s)")
    ax3.set_xlim([0, 40])
    plt.colorbar(im3, ax=ax3, label="Power (dB)")

    # Panel 4: 2D CA-CFAR Detections & Threshold Overlay
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.imshow(
        dsp_results["rdm_power_db"],
        aspect="auto",
        origin="lower",
        extent=extent,
        cmap="gray_r",
        alpha=0.6
    )
    for det in dsp_results["raw_detections"]:
        ax4.scatter(det["range_m"], det["velocity_mps"], s=80, facecolors='none', edgecolors='red', lw=2, label="CFAR Detection" if "CFAR Detection" not in [l.get_label() for l in ax4.collections] else "")
    ax4.set_title(f"4. 2D CA-CFAR Target Detections ({len(dsp_results['raw_detections'])} Detections)", fontsize=11, fontweight="bold")
    ax4.set_xlabel("Range (m)")
    ax4.set_ylabel("Radial Velocity (m/s)")
    ax4.set_xlim([0, 40])
    ax4.grid(True, linestyle="--", alpha=0.5)
    ax4.legend(loc="upper right", fontsize=8)

    # Panel 5: Spatial AoA Spectra (MUSIC vs Capon Beamforming)
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.plot(angles_deg, music_spec_1 - np.max(music_spec_1), label=f"MUSIC (Peak: {est_angle_1:+.1f}°)", color="#9467bd", lw=2)
    ax5.plot(angles_deg, capon_spec_1 - np.max(capon_spec_1), label="Capon / MVDR", color="#8c564b", lw=1.5, linestyle="--")
    ax5.set_title(f"5. Angle of Arrival (AoA) Spectra for Target #1", fontsize=11, fontweight="bold")
    ax5.set_xlabel("Azimuth Angle (degrees)")
    ax5.set_ylabel("Normalized Pseudo-Spectrum (dB)")
    ax5.set_xlim([-60, 60])
    ax5.set_ylim([-30, 2])
    ax5.grid(True, linestyle="--", alpha=0.5)
    ax5.legend(loc="upper right", fontsize=8)

    # Panel 6: Cartesian Bird's-Eye View (BEV) Clustered Objects
    ax6 = fig.add_subplot(gs[1, 2])
    # Plot Ground Truth targets
    for t in targets:
        gx = t.range_m * np.sin(np.deg2rad(t.azimuth_deg))
        gy = t.range_m * np.cos(np.deg2rad(t.azimuth_deg))
        ax6.scatter(gx, gy, marker="*", s=140, color="green", label="Ground Truth" if "Ground Truth" not in [l.get_label() for l in ax6.collections] else "")
        ax6.text(gx + 0.5, gy, f"{t.label} ({t.velocity_mps:+.1f}m/s)", fontsize=8, color="darkgreen", fontweight="bold")

    # Plot Clustered Objects
    for obj in dsp_results["detected_objects"]:
        ax6.scatter(obj["x_m"], obj["y_m"], marker="o", s=90, color="blue", label="DSP Estimated Object" if "DSP Estimated Object" not in [l.get_label() for l in ax6.collections] else "")
        ax6.plot([0, obj["x_m"]], [0, obj["y_m"]], color="blue", linestyle=":", alpha=0.4)

    ax6.scatter(0, 0, marker="^", s=150, color="black", label="Radar Sensor")
    ax6.set_title("6. Cartesian Bird's-Eye View (BEV) Tracking", fontsize=11, fontweight="bold")
    ax6.set_xlabel("Cross-Range X (meters)")
    ax6.set_ylabel("Down-Range Y (meters)")
    ax6.set_xlim([-20, 20])
    ax6.set_ylim([0, 35])
    ax6.grid(True, linestyle="--", alpha=0.5)
    ax6.legend(loc="lower right", fontsize=8)

    # Panel 7: Micro-Doppler Time-Frequency Signature
    ax7 = fig.add_subplot(gs[2, 0])
    im7 = ax7.imshow(
        md_spec,
        aspect="auto",
        origin="lower",
        extent=[md_times[0], md_times[-1], md_freqs[0], md_freqs[-1]],
        cmap="inferno"
    )
    ax7.set_title("7. Micro-Doppler Spectrogram (Pedestrian Gait)", fontsize=11, fontweight="bold")
    ax7.set_xlabel("Time (s)")
    ax7.set_ylabel("Doppler Frequency (Hz)")
    plt.colorbar(im7, ax=ax7, label="Power (dB)")

    # Panel 8: Deep Learning Detector Training Loss
    ax8 = fig.add_subplot(gs[2, 1])
    ax8.plot(range(1, len(history["train_loss"]) + 1), history["train_loss"], marker="o", label="Train Loss", color="#1f77b4", lw=2)
    ax8.plot(range(1, len(history["val_loss"]) + 1), history["val_loss"], marker="s", label="Val Loss", color="#ff7f0e", lw=2)
    ax8.set_title("8. Radar CNN Detector Training Convergence", fontsize=11, fontweight="bold")
    ax8.set_xlabel("Epoch")
    ax8.set_ylabel("Multi-Task Loss")
    ax8.grid(True, linestyle="--", alpha=0.5)
    ax8.legend(loc="upper right", fontsize=8)

    # Panel 9: Deep Learning Prediction Heatmap
    ax9 = fig.add_subplot(gs[2, 2])
    im9 = ax9.imshow(
        car_heatmap + ped_heatmap,
        aspect="auto",
        origin="lower",
        extent=extent,
        cmap="magma"
    )
    ax9.set_title("9. AI Deep Learning Output Detection Heatmap", fontsize=11, fontweight="bold")
    ax9.set_xlabel("Range (m)")
    ax9.set_ylabel("Radial Velocity (m/s)")
    ax9.set_xlim([0, 40])
    plt.colorbar(im9, ax=ax9, label="Detection Confidence")

    # Save output plot
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    plot_path = os.path.join(output_dir, "radar_pipeline_eda.png")
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()
    print(f"\n[+] High-Resolution EDA Plot successfully saved to: {os.path.abspath(plot_path)}")

    # Also copy to artifacts directory for display
    artifact_dir = r"C:\Users\Aryan Gupta\.gemini\antigravity-ide\brain\53c4d269-6a11-4f43-8d8b-f8cc1f4b5ec7"
    if os.path.exists(artifact_dir):
        import shutil
        shutil.copy(plot_path, os.path.join(artifact_dir, "radar_pipeline_eda.png"))
        print(f"[+] Synced plot to artifacts directory: {artifact_dir}")

    print("\n" + "=" * 80)
    print("      RADAR PIPELINE EXECUTION & VALIDATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    run_full_pipeline()
