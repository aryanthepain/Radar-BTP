"""
Comprehensive DSP Edge Cases Test Suite
Targets edge cases, alternate windowing functions, CFAR variants (GOCA/SOCA/OS),
AoA rank-deficient matrix handling, MTI filtering modes, and DBSCAN boundary conditions.
"""
import os
import sys
import unittest
import numpy as np

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sim.radar_config import RadarConfig
from src.dsp.range_processing import RangeProcessor
from src.dsp.clutter_removal import ClutterFilter
from src.dsp.doppler_processing import DopplerProcessor
from src.dsp.cfar_detector import CFARDetector2D
from src.dsp.aoa_estimation import AngleEstimator
from src.dsp.clustering import RadarClusterer

class TestDSPEdgeCases(unittest.TestCase):

    def setUp(self):
        self.config = RadarConfig(
            num_samples=128,
            num_chirps=64,
            num_rx=4,
            sampling_rate=10e6,
            chirp_duration=30e-6,
            bandwidth=150e6
        )

    def test_range_processor_windows_and_scaling(self):
        """Exercises alternate windowing functions and get_magnitude_db."""
        for win in ["hamming", "blackman", "boxcar", "rect", "unknown_window"]:
            rp = RangeProcessor(self.config, window=win)
            self.assertEqual(len(rp.window), self.config.num_samples)

        rp = RangeProcessor(self.config, window="hamming", n_fft=256)
        dummy_cube = np.random.randn(self.config.num_rx, self.config.num_chirps, self.config.num_samples) + \
                     1j * np.random.randn(self.config.num_rx, self.config.num_chirps, self.config.num_samples)
        profile, axis = rp.process(dummy_cube)
        self.assertEqual(profile.shape, (self.config.num_rx, self.config.num_chirps, 256))
        self.assertEqual(len(axis), self.config.num_samples)

        mag_db = rp.get_magnitude_db(profile)
        self.assertEqual(mag_db.shape, profile.shape)
        self.assertTrue(np.all(np.isfinite(mag_db)))

    def test_clutter_filter_modes(self):
        """Exercises 2pulse, 3pulse, highpass, unknown fallback, and attenuation edge cases."""
        dummy_data = np.random.randn(4, 32, 64) + 1j * np.random.randn(4, 32, 64)
        
        # 2-pulse MTI
        cf_2p = ClutterFilter(method="2pulse_mti")
        out_2p = cf_2p.filter(dummy_data, slow_time_axis=1)
        self.assertEqual(out_2p.shape, dummy_data.shape)

        # 3-pulse MTI
        cf_3p = ClutterFilter(method="3pulse_mti")
        out_3p = cf_3p.filter(dummy_data, slow_time_axis=1)
        self.assertEqual(out_3p.shape, dummy_data.shape)

        # Highpass Butterworth
        cf_hp = ClutterFilter(method="highpass", highpass_cutoff=0.1)
        out_hp = cf_hp.filter(dummy_data, slow_time_axis=1)
        self.assertEqual(out_hp.shape, dummy_data.shape)

        # Fallback
        cf_none = ClutterFilter(method="unknown_method")  # type: ignore
        out_none = cf_none.filter(dummy_data)
        np.testing.assert_array_equal(out_none, dummy_data)

        # Attenuation calculation
        att_db = ClutterFilter.compute_clutter_attenuation_db(dummy_data, out_2p)
        self.assertTrue(np.isfinite(att_db))

        # Zero energy filtered signal
        zero_filt = np.zeros_like(dummy_data)
        self.assertEqual(ClutterFilter.compute_clutter_attenuation_db(dummy_data, zero_filt), 100.0)

    def test_doppler_processor_edge_cases(self):
        """Exercises DopplerProcessor alternate windows, power averaging, and micro-Doppler STFT."""
        for win in ["hamming", "blackman", "boxcar", "rect", "invalid_win"]:
            dp = DopplerProcessor(self.config, window=win)
            self.assertEqual(len(dp.window), self.config.num_chirps)

        dp = DopplerProcessor(self.config, window="blackman", n_fft=128)
        range_cube = np.random.randn(4, self.config.num_chirps, 128) + 1j * np.random.randn(4, self.config.num_chirps, 128)
        rdm, v_axis, r_axis = dp.process(range_cube)
        self.assertEqual(rdm.shape, (4, 128, 128))

        # Power dB for specific Rx antenna
        p_rx0 = dp.get_power_db(rdm, rx_index=0)
        self.assertEqual(p_rx0.shape, (128, 128))

        # Power dB averaged across all Rx
        p_avg = dp.get_power_db(rdm, rx_index=None)
        self.assertEqual(p_avg.shape, (128, 128))
        self.assertTrue(np.all(np.isfinite(p_avg)))

        # Micro-Doppler spectrogram STFT
        slow_time_sig = np.sin(2 * np.pi * 50 * np.linspace(0, 1, 512)) + 0.1 * np.random.randn(512)
        freqs, times, spec = DopplerProcessor.compute_micro_doppler_spectrogram(slow_time_sig, fs=1000.0, nperseg=64, noverlap=32)
        self.assertEqual(spec.shape, (len(freqs), len(times)))
        self.assertTrue(np.all(np.isfinite(spec)))

    def test_cfar_variants_and_boundaries(self):
        """Exercises GOCA, SOCA, OS-CFAR, fallback CFAR, and boundary conditions."""
        power_map = np.ones((32, 32)) * 0.01
        # Insert known target peak
        power_map[16, 16] = 50.0

        # OS-CFAR
        cfar_os = CFARDetector2D(num_train_range=4, num_train_doppler=4, cfar_type="os", os_rank_k=10)
        mask_os, thresh_os, dets_os = cfar_os.detect(power_map)
        self.assertTrue(mask_os[16, 16])
        self.assertGreater(len(dets_os), 0)

        # GOCA-CFAR
        cfar_goca = CFARDetector2D(num_train_range=4, num_train_doppler=4, cfar_type="goca")
        mask_goca, thresh_goca, dets_goca = cfar_goca.detect(power_map)
        self.assertTrue(mask_goca[16, 16])

        # SOCA-CFAR
        cfar_soca = CFARDetector2D(num_train_range=4, num_train_doppler=4, cfar_type="soca")
        mask_soca, thresh_soca, dets_soca = cfar_soca.detect(power_map)
        self.assertTrue(mask_soca[16, 16])

        # Fallback CFAR type with axis=None
        cfar_fb = CFARDetector2D(cfar_type="unknown_cfar")  # type: ignore
        mask_fb, thresh_fb, dets_fb = cfar_fb.detect(power_map, range_axis=None, velocity_axis=None)
        self.assertTrue(mask_fb[16, 16])
        self.assertEqual(dets_fb[0]["range_m"], 16.0)

        # Zero training cells edge case
        cfar_zero = CFARDetector2D(num_train_range=0, num_train_doppler=0)
        self.assertEqual(cfar_zero.alpha_ca, 1.0)

    def test_aoa_estimation_edge_cases(self):
        """Exercises 1D signals and single-snapshot inputs for AoA estimators."""
        estimator = AngleEstimator(self.config, num_angle_bins=90)

        # 1D single-snapshot FFT
        rx_1d = np.exp(1j * np.pi * 0.3 * np.arange(self.config.num_rx))
        angles, spec_fft, peak_fft = estimator.estimate_aoa_fft(rx_1d, n_fft=64)
        self.assertTrue(np.isfinite(peak_fft))

        # 1D single-snapshot Capon
        angles, spec_capon, peak_capon = estimator.estimate_aoa_capon(rx_1d)
        self.assertEqual(len(angles), 90)
        self.assertTrue(np.isfinite(peak_capon))

        # 1D single-snapshot MUSIC
        angles, spec_music, peak_music = estimator.estimate_aoa_music(rx_1d, num_sources=1)
        self.assertEqual(len(angles), 90)
        self.assertTrue(np.isfinite(peak_music))

        # MUSIC with num_sources >= num_rx (boundary condition)
        angles, spec_m_bound, peak_m_bound = estimator.estimate_aoa_music(rx_1d, num_sources=self.config.num_rx)
        self.assertTrue(np.isfinite(peak_m_bound))

    def test_radar_clusterer_edge_cases(self):
        """Exercises empty detections, single detection, and missing azimuth key."""
        clusterer = RadarClusterer(eps=2.0, min_samples=1)

        # Empty detections
        self.assertEqual(clusterer.cluster_detections([]), [])

        # Single detection
        det_single = [{
            "range_m": 10.0,
            "velocity_mps": 2.5,
            "peak_power": 15.0
            # Note: azimuth_deg omitted to test default .get("azimuth_deg", 0.0)
        }]
        clusters = clusterer.cluster_detections(det_single)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(clusters[0]["num_points"], 1)
        self.assertAlmostEqual(clusters[0]["range_m"], 10.0, places=2)

        # Multi-point cluster with noise points
        clusterer_noise = RadarClusterer(eps=0.5, min_samples=3)
        dets_multi = [
            {"range_m": 10.0, "velocity_mps": 0.0, "azimuth_deg": 0.0, "peak_power": 10.0},
            {"range_m": 50.0, "velocity_mps": 15.0, "azimuth_deg": 30.0, "peak_power": 5.0}  # Isolated noise point
        ]
        clusters_noise = clusterer_noise.cluster_detections(dets_multi)
        # Both should be classified as noise (-1) and filtered out
        self.assertEqual(len(clusters_noise), 0)

if __name__ == "__main__":
    unittest.main()
