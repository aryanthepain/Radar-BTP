"""
Range Processing Module for FMCW Radar
Computes 1D Fast-Time Range FFT with windowing to produce calibrated 1D Range Profiles.
"""
from typing import Tuple, Optional
import numpy as np
from src.sim.radar_config import RadarConfig

class RangeProcessor:
    """
    Applies windowing and 1D Fast-Time FFT along the ADC sample dimension of a radar cube.
    """

    def __init__(self, config: Optional[RadarConfig] = None, window: str = "hann", n_fft: Optional[int] = None):
        self.config = config or RadarConfig()
        self.window_type = window
        self.n_fft = n_fft or self.config.num_samples
        self.window = self._get_window(self.config.num_samples, window)
        self.range_axis = self.config.get_range_axis()

    def _get_window(self, num_samples: int, window: str) -> np.ndarray:
        if window == "hann":
            return np.hanning(num_samples)
        elif window == "hamming":
            return np.hamming(num_samples)
        elif window == "blackman":
            return np.blackman(num_samples)
        elif window == "boxcar" or window == "rect":
            return np.ones(num_samples)
        else:
            return np.hanning(num_samples)

    def process(self, radar_cube: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Processes radar cube of shape (num_rx, num_chirps, num_samples).
        
        Returns:
            range_profile: Complex ndarray of shape (num_rx, num_chirps, num_range_bins).
            range_axis: 1D array of range values in meters.
        """
        # Apply window along fast-time axis (last axis)
        windowed = radar_cube * self.window[np.newaxis, np.newaxis, :]
        
        # Complex 1D FFT along fast-time axis across all complex sample bins
        range_profile = np.fft.fft(windowed, n=self.n_fft, axis=-1)
        
        return range_profile, self.range_axis

    def get_magnitude_db(self, range_profile: np.ndarray) -> np.ndarray:
        """Computes power in dB scale."""
        mag = np.abs(range_profile)
        # Avoid log(0)
        return 20.0 * np.log10(np.maximum(mag, 1e-12))
