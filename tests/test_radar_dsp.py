"""
Deterministic Unit Tests for FMCW Radar DSP Primitives and Neural Network Detector
"""
import os
import sys
import warnings

# Suppress joblib loky physical core detection warning on Windows
_n_cpus = os.cpu_count() or 4
os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(max(_n_cpus - 1, 1)))
warnings.filterwarnings("ignore", message=r".*Could not find the number of physical cores.*")
warnings.filterwarnings("ignore", module=r".*loky.*")

import unittest
import numpy as np
import torch

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sim.radar_config import RadarConfig, SPEED_OF_LIGHT
from src.sim.target import RadarTarget
from src.sim.radar_sim import FMCWRadarSimulator
from src.dsp.range_processing import RangeProcessor
from src.dsp.clutter_removal import ClutterFilter
from src.dsp.doppler_processing import DopplerProcessor
from src.dsp.cfar_detector import CFARDetector2D
from src.dsp.aoa_estimation import AngleEstimator
from src.dsp.clustering import RadarClusterer
from src.dsp.radar_pipeline import ClassicalRadarPipeline
from src.models.radar_detector_cnn import RadarObjectDetectorCNN, NUM_CLASSES

class TestRadarDSP(unittest.TestCase):

    def setUp(self):
        self.config = RadarConfig(
            fc=77e9,
            bandwidth=1.0e9,
            chirp_duration=50e-6,
            num_samples=256,
            num_chirps=128,
            num_rx=4,
            sampling_rate=5.12e6
        )
        self.sim = FMCWRadarSimulator(self.config)

    def test_radar_config_physics(self):
        """Validates fundamental radar equations."""
        cfg = self.config
        expected_lambda = SPEED_OF_LIGHT / 77e9
        self.assertAlmostEqual(cfg.wavelength, expected_lambda, places=6)

        expected_delta_r = SPEED_OF_LIGHT / (2.0 * 1.0e9) # 0.149896 m
        self.assertAlmostEqual(cfg.range_resolution, expected_delta_r, places=4)

        expected_delta_v = cfg.wavelength / (2.0 * 128 * 50e-6) # ~0.304 m/s
        self.assertAlmostEqual(cfg.velocity_resolution, expected_delta_v, places=3)

    def test_range_fft_accuracy(self):
        """Verifies 1D Fast-Time Range FFT recovers target range within theoretical resolution."""
        target_range = 22.5
        target = RadarTarget(range_m=target_range, velocity_mps=0.0, azimuth_deg=0.0, rcs_dbsm=10.0)
        cube = self.sim.generate_radar_cube([target], snr_db=30.0, include_clutter=False, seed=42)

        range_proc = RangeProcessor(self.config)
        range_cube, range_axis = range_proc.process(cube)

        # Average power across Rx and chirps
        range_power = np.mean(np.abs(range_cube)**2, axis=(0, 1))
        peak_idx = np.argmax(range_power)
        estimated_range = range_axis[peak_idx]

        # Estimation error must be smaller than range resolution
        err = abs(estimated_range - target_range)
        self.assertLess(err, self.config.range_resolution)

    def test_doppler_fft_accuracy(self):
        """Verifies 2D Slow-Time Doppler FFT recovers target radial velocity within resolution."""
        target_range = 15.0
        target_velocity = 8.5 # m/s
        target = RadarTarget(range_m=target_range, velocity_mps=target_velocity, azimuth_deg=0.0, rcs_dbsm=10.0)
        cube = self.sim.generate_radar_cube([target], snr_db=30.0, include_clutter=False, seed=42)

        range_proc = RangeProcessor(self.config)
        range_cube, range_axis = range_proc.process(cube)

        doppler_proc = DopplerProcessor(self.config)
        rdm, velocity_axis, _ = doppler_proc.process(range_cube)

        rdm_power = np.mean(np.abs(rdm)**2, axis=0) # (num_doppler, num_range)
        d_idx, r_idx = np.unravel_index(np.argmax(rdm_power), rdm_power.shape)

        est_vel = velocity_axis[d_idx]
        err_v = abs(est_vel - target_velocity)
        self.assertLess(err_v, self.config.velocity_resolution * 1.5)

    def test_clutter_filter_attenuation(self):
        """Verifies MTI mean subtraction provides > 15 dB clutter attenuation on stationary targets."""
        stationary_target = RadarTarget(range_m=10.0, velocity_mps=0.0, azimuth_deg=0.0, rcs_dbsm=20.0)
        cube = self.sim.generate_radar_cube([stationary_target], snr_db=20.0, include_clutter=True, seed=42)

        range_proc = RangeProcessor(self.config)
        range_cube, _ = range_proc.process(cube)

        clutter_filter = ClutterFilter(method="mean_subtraction")
        filtered_cube = clutter_filter.filter(range_cube, slow_time_axis=1)

        ca_db = ClutterFilter.compute_clutter_attenuation_db(range_cube, filtered_cube)
        self.assertGreater(ca_db, 15.0)

    def test_cfar_detector_2d(self):
        """Verifies 2D CA-CFAR detects target peak above adaptive noise floor."""
        target = RadarTarget(range_m=18.0, velocity_mps=-6.0, azimuth_deg=0.0, rcs_dbsm=15.0)
        cube = self.sim.generate_radar_cube([target], snr_db=20.0, include_clutter=False, seed=42)

        pipeline = ClassicalRadarPipeline(config=self.config, cfar_type="ca", p_fa=1e-4)
        results = pipeline.process_radar_cube(cube)

        self.assertGreater(len(results["raw_detections"]), 0)
        closest_det = min(results["raw_detections"], key=lambda d: abs(d["range_m"] - 18.0))
        self.assertLess(abs(closest_det["range_m"] - 18.0), self.config.range_resolution)
        self.assertLess(abs(closest_det["velocity_mps"] - (-6.0)), self.config.velocity_resolution * 1.5)

    def test_music_aoa_estimation(self):
        """Verifies MUSIC subspace algorithm accurately resolves azimuth angle."""
        target_angle = -20.0 # deg
        target = RadarTarget(range_m=20.0, velocity_mps=5.0, azimuth_deg=target_angle, rcs_dbsm=15.0)
        cube = self.sim.generate_radar_cube([target], snr_db=25.0, include_clutter=False, seed=42)

        pipeline = ClassicalRadarPipeline(config=self.config)
        results = pipeline.process_radar_cube(cube)

        self.assertGreater(len(results["raw_detections"]), 0)
        est_angle = results["raw_detections"][0]["azimuth_deg"]
        angle_error = abs(est_angle - target_angle)
        self.assertLess(angle_error, 2.0) # Accuracy within 2 degrees

    def test_radar_cnn_forward_and_loss(self):
        """Verifies PyTorch RadarObjectDetectorCNN forward pass, multi-task loss, and backpropagation."""
        model = RadarObjectDetectorCNN(in_channels=1, num_classes=NUM_CLASSES, base_filters=16)
        dummy_input = torch.randn(2, 1, 128, 129)
        cls_logits, box_preds = model(dummy_input)

        self.assertEqual(cls_logits.shape, (2, NUM_CLASSES, 128, 129))
        self.assertEqual(box_preds.shape, (2, 4, 128, 129))

        dummy_heatmap = torch.zeros(2, NUM_CLASSES, 128, 129)
        dummy_boxes = torch.zeros(2, 4, 128, 129)
        loss, cls_loss, box_loss = model.compute_loss(cls_logits, box_preds, dummy_heatmap, dummy_boxes)

        self.assertFalse(torch.isnan(loss))
        loss.backward()

        # Ensure gradients are computed
        grad_norm = sum(p.grad.norm().item() for p in model.parameters() if p.grad is not None)
        self.assertGreater(grad_norm, 0.0)

if __name__ == "__main__":
    unittest.main()
