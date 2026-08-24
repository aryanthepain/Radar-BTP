"""
High-Fidelity FMCW Radar Raw ADC Signal Generator
Simulates complex baseband I/Q dechirped beat signals for multi-target scenarios with clutter and noise.
"""
from typing import List, Optional
import numpy as np
from src.sim.radar_config import RadarConfig, SPEED_OF_LIGHT
from src.sim.target import RadarTarget

class FMCWRadarSimulator:
    """
    Simulates raw time-domain I/Q ADC data from FMCW radar chirps.
    Output data structure: Radar Cube of shape (num_rx, num_chirps, num_samples).
    """

    def __init__(self, config: Optional[RadarConfig] = None):
        self.config = config or RadarConfig()

    def generate_radar_cube(
        self,
        targets: List[RadarTarget],
        snr_db: float = 20.0,
        clutter_ratio_db: float = 10.0,
        include_clutter: bool = True,
        seed: Optional[int] = 42
    ) -> np.ndarray:
        """
        Synthesizes the 3D complex baseband radar cube.
        
        Args:
            targets: List of RadarTarget objects in the field of view.
            snr_db: Signal-to-Noise Ratio (dB) referenced to 0 dBsm target.
            clutter_ratio_db: Clutter-to-Noise Ratio (dB) for stationary clutter.
            include_clutter: Whether to inject stationary ground/wall clutter.
            seed: Random seed for reproducibility.
            
        Returns:
            radar_cube: Complex ndarray of shape (num_rx, num_chirps, num_samples).
        """
        if seed is not None:
            np.random.seed(seed)

        cfg = self.config
        num_rx = cfg.num_rx
        num_chirps = cfg.num_chirps
        num_samples = cfg.num_samples

        # Time vectors
        # Fast-time (within single chirp): t_fast in [0, Tc)
        t_fast = np.arange(num_samples) / cfg.sampling_rate  # shape: (num_samples,)
        # Slow-time (chirp start times): t_slow in [0, num_chirps * Tc)
        t_slow = np.arange(num_chirps) * cfg.chirp_duration   # shape: (num_chirps,)
        # Receiver antenna spatial indices: 0, 1, ..., num_rx - 1
        rx_idx = np.arange(num_rx)                           # shape: (num_rx,)

        # Meshgrid / broadcast shapes: (num_rx, num_chirps, num_samples)
        # We construct 3D arrays:
        rx_grid = rx_idx[:, np.newaxis, np.newaxis]       # (num_rx, 1, 1)
        slow_grid = t_slow[np.newaxis, :, np.newaxis]     # (1, num_chirps, 1)
        fast_grid = t_fast[np.newaxis, np.newaxis, :]     # (1, 1, num_samples)

        radar_cube = np.zeros((num_rx, num_chirps, num_samples), dtype=np.complex128)

        wavelength = cfg.wavelength
        slope = cfg.chirp_slope
        ant_spacing = cfg.antenna_spacing

        # Superpose target beat signals
        for target in targets:
            # Range at slow-time t_slow: R(t_slow) = R_0 - v * t_slow (approaching is +, decreasing range)
            # Velocity: v > 0 means approaching, Doppler frequency f_d = +2*v/lambda
            r_0 = target.range_m
            v_0 = target.velocity_mps
            theta_rad = np.deg2rad(target.azimuth_deg)

            # Instantaneous range accounting for constant velocity
            r_t = r_0 - v_0 * slow_grid

            # Micro-Doppler modulation if present
            if target.micro_doppler_freq and target.micro_doppler_amp:
                f_md = target.micro_doppler_freq
                a_md = target.micro_doppler_amp
                r_t += (a_md / (2 * np.pi * f_md)) * np.sin(2 * np.pi * f_md * slow_grid)

            # 1. Beat frequency along fast-time: f_b = 2 * S * r_t / c
            # Fast-time phase: 2 * pi * f_b * t_fast
            phase_fast = 2.0 * np.pi * (2.0 * slope * r_t / SPEED_OF_LIGHT) * fast_grid

            # 2. Doppler phase shift across slow-time: phi_doppler = 2 * pi * (2 * v_0 / lambda) * t_slow
            phase_doppler = 2.0 * np.pi * (2.0 * v_0 / wavelength) * slow_grid

            # 3. Spatial angle phase shift across ULA elements: phi_rx = 2 * pi * (d * sin(theta) / lambda) * rx_idx
            phase_spatial = 2.0 * np.pi * (ant_spacing * np.sin(theta_rad) / wavelength) * rx_grid

            # 4. Carrier range phase: 4 * pi * R_0 / lambda
            phase_carrier = 4.0 * np.pi * r_0 / wavelength

            total_phase = phase_fast + phase_doppler + phase_spatial + phase_carrier

            # Target amplitude proportional to sqrt(RCS) and inverse-square path loss: 1 / R^2
            amplitude = np.sqrt(target.rcs_linear) / max(r_0**2, 1.0)
            target_signal = amplitude * np.exp(1j * total_phase)
            radar_cube += target_signal

        # Normalize target signal power
        signal_power = np.mean(np.abs(radar_cube)**2)
        if signal_power > 0:
            scale_factor = 1.0 / np.sqrt(signal_power)
            radar_cube *= scale_factor

        # Add stationary ground/environmental clutter (Zero-Doppler, wide range spread)
        if include_clutter:
            # Clutter power based on CNR (Clutter-to-Noise Ratio)
            clutter_power = 10.0 ** (clutter_ratio_db / 10.0)
            # Create random stationary reflectors across range bins
            num_clutter_points = 50
            clutter_ranges = np.random.uniform(1.0, cfg.max_unambiguous_range * 0.8, size=num_clutter_points)
            clutter_amplitudes = np.random.rayleigh(scale=np.sqrt(clutter_power / num_clutter_points), size=num_clutter_points)
            clutter_angles = np.random.uniform(-np.pi/3, np.pi/3, size=num_clutter_points)

            clutter_signal = np.zeros_like(radar_cube)
            for c_r, c_amp, c_th in zip(clutter_ranges, clutter_amplitudes, clutter_angles):
                c_phase_fast = 2.0 * np.pi * (2.0 * slope * c_r / SPEED_OF_LIGHT) * fast_grid
                c_phase_spatial = 2.0 * np.pi * (ant_spacing * np.sin(c_th) / wavelength) * rx_grid
                # Stationary => zero Doppler phase shift over slow-time
                clutter_signal += c_amp * np.exp(1j * (c_phase_fast + c_phase_spatial + np.random.uniform(0, 2*np.pi)))
            radar_cube += clutter_signal

        # Add Thermal Noise (Complex AWGN)
        # Noise power referenced to unit signal power: P_noise = 10^(-SNR/10)
        noise_power = 10.0 ** (-snr_db / 10.0)
        noise = np.sqrt(noise_power / 2.0) * (
            np.random.randn(*radar_cube.shape) + 1j * np.random.randn(*radar_cube.shape)
        )
        radar_cube += noise

        return radar_cube
