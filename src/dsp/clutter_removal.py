"""
Clutter Removal and Moving Target Indication (MTI) Filter Module
Suppresses stationary ground, wall, and environmental clutter while preserving moving targets.
"""
from typing import Literal
import numpy as np
from scipy import signal

class ClutterFilter:
    """
    Implements classical MTI (Moving Target Indicator) and static clutter removal algorithms.
    """

    def __init__(self, method: Literal["mean_subtraction", "2pulse_mti", "3pulse_mti", "highpass"] = "mean_subtraction", highpass_cutoff: float = 0.05):
        self.method = method
        self.highpass_cutoff = highpass_cutoff

    def filter(self, data: np.ndarray, slow_time_axis: int = 1) -> np.ndarray:
        """
        Filters clutter along the slow-time (chirp) dimension.
        
        Args:
            data: Complex range profile or radar cube of shape (..., num_chirps, ...).
            slow_time_axis: Axis corresponding to chirps (slow-time).
            
        Returns:
            filtered_data: Clutter-suppressed complex array of matching shape.
        """
        if self.method == "mean_subtraction":
            # Subtract mean across chirps (removes zero-Doppler static reflection)
            mean_signal = np.mean(data, axis=slow_time_axis, keepdims=True)
            return data - mean_signal

        elif self.method == "2pulse_mti":
            # Delay-line canceller: y[m] = x[m] - x[m-1]
            # Difference along slow-time axis
            diff = np.diff(data, axis=slow_time_axis, prepend=np.take(data, [0], axis=slow_time_axis))
            return diff

        elif self.method == "3pulse_mti":
            # 3-pulse canceller: y[m] = x[m] - 2*x[m-1] + x[m-2]
            # Finite difference weights: [1, -2, 1]
            weights = np.array([1.0, -2.0, 1.0])
            # Apply convolution along slow_time_axis
            filtered = np.apply_along_axis(lambda m: np.convolve(m, weights, mode='same'), slow_time_axis, data)
            return filtered

        elif self.method == "highpass":
            # High-pass Butterworth filter across slow time
            b, a = signal.butter(4, self.highpass_cutoff, btype='high', analog=False)
            filtered = signal.filtfilt(b, a, data, axis=slow_time_axis)
            return filtered

        else:
            return data

    @staticmethod
    def compute_clutter_attenuation_db(raw_data: np.ndarray, filtered_data: np.ndarray) -> float:
        """
        Computes total energy suppression ratio in dB.
        CA (dB) = 10 * log10(Power_raw / Power_filtered)
        """
        raw_power = np.mean(np.abs(raw_data)**2)
        filt_power = np.mean(np.abs(filtered_data)**2)
        if filt_power <= 0:
            return 100.0
        return 10.0 * np.log10(raw_power / filt_power)
