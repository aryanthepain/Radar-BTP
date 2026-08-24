"""
FMCW Radar Configuration and Physics Constants
"""
import numpy as np
from dataclasses import dataclass

# Physical constants
SPEED_OF_LIGHT = 299792458.0  # m/s

@dataclass
class RadarConfig:
    """
    Configuration parameters for an FMCW Radar System.
    Default parameters model a typical 77 GHz automotive / mmWave radar (e.g. TI AWR1843).
    """
    fc: float = 77e9               # Center carrier frequency (Hz) -> 77 GHz
    bandwidth: float = 1.0e9       # Chirp sweep bandwidth (Hz) -> 1 GHz
    chirp_duration: float = 50e-6  # Active chirp duration Tc (seconds) -> 50 us
    num_samples: int = 256         # Number of ADC fast-time samples per chirp
    num_chirps: int = 128          # Number of slow-time chirps in a frame
    num_rx: int = 4                # Number of receiver antennas in uniform linear array (ULA)
    rx_spacing_factor: float = 0.5 # Antenna spacing in wavelengths (d = 0.5 * lambda)
    sampling_rate: float = 5.12e6  # ADC sampling rate Fs (Hz) -> 5.12 MHz

    @property
    def wavelength(self) -> float:
        """Operating wavelength (lambda = c / fc)."""
        return SPEED_OF_LIGHT / self.fc

    @property
    def antenna_spacing(self) -> float:
        """Physical spacing between adjacent receiver antennas (d)."""
        return self.rx_spacing_factor * self.wavelength

    @property
    def chirp_slope(self) -> float:
        """Chirp frequency slope S = Bandwidth / Tc (Hz/s)."""
        return self.bandwidth / self.chirp_duration

    @property
    def range_resolution(self) -> float:
        """Theoretical range resolution delta_R = c / (2 * B) (meters)."""
        return SPEED_OF_LIGHT / (2.0 * self.bandwidth)

    @property
    def max_unambiguous_range(self) -> float:
        """Maximum unambiguous range R_max = (Fs * c) / (2 * S) (meters)."""
        return (self.sampling_rate * SPEED_OF_LIGHT) / (2.0 * self.chirp_slope)

    @property
    def velocity_resolution(self) -> float:
        """Theoretical velocity resolution delta_v = lambda / (2 * N_chirps * Tc) (m/s)."""
        return self.wavelength / (2.0 * self.num_chirps * self.chirp_duration)

    @property
    def max_unambiguous_velocity(self) -> float:
        """Maximum unambiguous velocity v_max = lambda / (4 * Tc) (m/s)."""
        return self.wavelength / (4.0 * self.chirp_duration)

    @property
    def frame_duration(self) -> float:
        """Total frame duration (seconds)."""
        return self.num_chirps * self.chirp_duration

    def get_range_axis(self) -> np.ndarray:
        """Returns physical range bins (meters) for Complex Fast-Time Range FFT."""
        freq_axis = np.arange(self.num_samples) * (self.sampling_rate / self.num_samples)
        return (freq_axis * SPEED_OF_LIGHT) / (2.0 * self.chirp_slope)

    def get_velocity_axis(self) -> np.ndarray:
        """Returns physical velocity bins (m/s) for Doppler FFT output centered at 0."""
        doppler_freqs = np.fft.fftshift(np.fft.fftfreq(self.num_chirps, d=self.chirp_duration))
        return (doppler_freqs * self.wavelength) / 2.0

    def get_angle_axis(self, num_angle_bins: int = 180) -> np.ndarray:
        """Returns angle bins in degrees (-90 to +90)."""
        return np.linspace(-90.0, 90.0, num_angle_bins)
