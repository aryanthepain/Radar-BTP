"""
Doppler Processing and Range-Doppler Matrix (RDM) Module
Computes 2D FFT across slow-time chirps and fast-time samples to map Target Range vs. Radial Velocity.
Also computes Micro-Doppler time-frequency signatures via STFT.
"""
from typing import Tuple, Optional
import numpy as np
from scipy import signal
from src.sim.radar_config import RadarConfig

class DopplerProcessor:
    """
    Computes Doppler FFT along the slow-time (chirp) axis to produce 2D Range-Doppler Matrices.
    """

    def __init__(self, config: Optional[RadarConfig] = None, window: str = "hann", n_fft: Optional[int] = None):
        self.config = config or RadarConfig()
        self.window_type = window
        self.n_fft = n_fft or self.config.num_chirps
        self.window = self._get_window(self.config.num_chirps, window)
        self.velocity_axis = self.config.get_velocity_axis()
        self.range_axis = self.config.get_range_axis()

    def _get_window(self, num_chirps: int, window: str) -> np.ndarray:
        if window == "hann":
            return np.hanning(num_chirps)
        elif window == "hamming":
            return np.hamming(num_chirps)
        elif window == "blackman":
            return np.blackman(num_chirps)
        elif window == "boxcar" or window == "rect":
            return np.ones(num_chirps)
        else:
            return np.hanning(num_chirps)

    def process(self, range_cube: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Processes range cube of shape (num_rx, num_chirps, num_range_bins).
        
        Returns:
            rdm: Complex ndarray of shape (num_rx, num_doppler_bins, num_range_bins).
            velocity_axis: 1D array of velocity values (m/s), centered around 0.
            range_axis: 1D array of range values (m).
        """
        # Window along slow-time (chirp) axis (axis=1)
        windowed = range_cube * self.window[np.newaxis, :, np.newaxis]
        
        # FFT along chirp axis
        doppler_fft = np.fft.fft(windowed, n=self.n_fft, axis=1)
        
        # Shift zero-Doppler frequency bin to center
        rdm = np.fft.fftshift(doppler_fft, axes=1)
        
        return rdm, self.velocity_axis, self.range_axis

    def get_power_db(self, rdm: np.ndarray, rx_index: int = 0) -> np.ndarray:
        """Computes power spectral density in dB for a specific Rx antenna or average across all Rx."""
        if rx_index is not None and rx_index >= 0:
            slice_data = rdm[rx_index]
        else:
            # Average power across all receiver antennas
            slice_data = np.mean(np.abs(rdm)**2, axis=0)
            return 10.0 * np.log10(np.maximum(slice_data, 1e-12))
            
        mag_sq = np.abs(slice_data)**2
        return 10.0 * np.log10(np.maximum(mag_sq, 1e-12))

    @staticmethod
    def compute_micro_doppler_spectrogram(
        slow_time_signal: np.ndarray,
        fs: float,
        nperseg: int = 64,
        noverlap: int = 48
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes STFT (Short-Time Fourier Transform) along continuous slow-time samples to visualize Micro-Doppler.
        
        Returns:
            freqs: Doppler frequencies (Hz).
            times: Time segment centers (s).
            spectrogram_db: Micro-Doppler power (dB).
        """
        f, t, zxx = signal.stft(slow_time_signal, fs=fs, nperseg=nperseg, noverlap=noverlap, return_onesided=False)
        f_shift = np.fft.fftshift(f)
        zxx_shift = np.fft.fftshift(zxx, axes=0)
        spec_db = 20.0 * np.log10(np.maximum(np.abs(zxx_shift), 1e-12))
        return f_shift, t, spec_db
