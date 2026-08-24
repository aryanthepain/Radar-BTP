"""
Angle of Arrival (AoA) and Direction of Arrival (DoA) Estimation Module
Implements Spatial FFT Beamforming, Capon (MVDR), and Subspace MUSIC Algorithms for ULA.
"""
from typing import Tuple, Optional, Literal
import numpy as np
from src.sim.radar_config import RadarConfig

class AngleEstimator:
    """
    Direction of Arrival (DoA) estimation across Uniform Linear Array (ULA) Rx antennas.
    """

    def __init__(self, config: Optional[RadarConfig] = None, num_angle_bins: int = 180):
        self.config = config or RadarConfig()
        self.num_angle_bins = num_angle_bins
        self.angles_deg = np.linspace(-90.0, 90.0, num_angle_bins)
        self.angles_rad = np.deg2rad(self.angles_deg)

        # Precompute steering vectors for all angles
        # a(theta) = exp(j * 2 * pi * d * sin(theta) / lambda * [0, 1, ..., N_rx - 1]^T)
        rx_indices = np.arange(self.config.num_rx)
        # Shape: (num_rx, num_angle_bins)
        phase_matrix = 2.0 * np.pi * (self.config.antenna_spacing / self.config.wavelength) * np.sin(self.angles_rad)[np.newaxis, :] * rx_indices[:, np.newaxis]
        self.steering_matrix = np.exp(1j * phase_matrix)  # (num_rx, num_angles)

    def estimate_aoa_fft(self, rx_signals: np.ndarray, n_fft: int = 128) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Conventional Spatial FFT Beamformer on antenna array snapshot.
        
        Args:
            rx_signals: 1D array of shape (num_rx,) or (num_rx, snapshots).
            
        Returns:
            angle_axis: 1D array of angles (degrees).
            spectrum_db: Angular spectrum in dB.
            peak_angle_deg: Estimated angle of highest peak.
        """
        if rx_signals.ndim == 2:
            sig = np.mean(rx_signals, axis=1)
        else:
            sig = rx_signals

        # Zero-pad and FFT along antenna dimension
        spatial_fft = np.fft.fftshift(np.fft.fft(sig, n=n_fft))
        mag = np.abs(spatial_fft)
        spectrum_db = 20.0 * np.log10(np.maximum(mag, 1e-12))
        
        # Spatial frequency to angle: sin(theta) = spatial_freq * lambda / d
        # spatial_freq in [-0.5, 0.5]
        freqs = np.fft.fftshift(np.fft.fftfreq(n_fft))
        sin_theta = freqs * (self.config.wavelength / self.config.antenna_spacing)
        # Clip to valid sine range
        valid = np.abs(sin_theta) <= 1.0
        angles = np.rad2deg(np.arcsin(sin_theta[valid]))
        spec = spectrum_db[valid]

        peak_idx = np.argmax(spec)
        return angles, spec, float(angles[peak_idx])

    def estimate_aoa_capon(self, rx_snapshots: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Capon (Minimum Variance Distortionless Response - MVDR) Beamforming.
        P_Capon(theta) = 1 / (a(theta)^H * R_xx^(-1) * a(theta))
        
        Args:
            rx_snapshots: 2D array of shape (num_rx, num_snapshots).
        """
        if rx_snapshots.ndim == 1:
            rx_snapshots = rx_snapshots[:, np.newaxis]

        num_rx, n_snap = rx_snapshots.shape
        # Spatial covariance matrix R_xx
        r_xx = (rx_snapshots @ rx_snapshots.conj().T) / max(n_snap, 1)
        # Diagonal loading for numerical stability
        r_xx += 1e-6 * np.eye(num_rx)
        r_inv = np.linalg.pinv(r_xx)

        spectrum = np.zeros(self.num_angle_bins, dtype=float)
        for i in range(self.num_angle_bins):
            a_theta = self.steering_matrix[:, i]  # (num_rx,)
            denom = np.real(a_theta.conj().T @ r_inv @ a_theta)
            spectrum[i] = 1.0 / max(denom, 1e-12)

        spectrum_db = 10.0 * np.log10(np.maximum(spectrum, 1e-12))
        peak_angle = float(self.angles_deg[np.argmax(spectrum_db)])
        return self.angles_deg, spectrum_db, peak_angle

    def estimate_aoa_music(self, rx_snapshots: np.ndarray, num_sources: int = 1) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        MUSIC (Multiple Signal Classification) Subspace High-Resolution Algorithm.
        P_MUSIC(theta) = 1 / (a(theta)^H * U_n * U_n^H * a(theta))
        
        Args:
            rx_snapshots: 2D array of shape (num_rx, num_snapshots).
            num_sources: Estimated number of signal sources (targets in same range-Doppler bin).
        """
        if rx_snapshots.ndim == 1:
            rx_snapshots = rx_snapshots[:, np.newaxis]

        num_rx, n_snap = rx_snapshots.shape
        # Sample covariance matrix
        r_xx = (rx_snapshots @ rx_snapshots.conj().T) / max(n_snap, 1)
        # Diagonal loading
        r_xx += 1e-6 * np.eye(num_rx)

        # Eigen-decomposition: eigh returns eigenvalues in ascending order
        eigenvalues, eigenvectors = np.linalg.eigh(r_xx)

        # Noise subspace U_n: eigenvectors corresponding to smallest (num_rx - num_sources) eigenvalues
        noise_dim = max(num_rx - num_sources, 1)
        u_n = eigenvectors[:, :noise_dim]  # shape: (num_rx, noise_dim)

        # Compute pseudo-spectrum
        # Denominator: a(theta)^H * U_n * U_n^H * a(theta) = || U_n^H * a(theta) ||^2
        un_h_a = u_n.conj().T @ self.steering_matrix  # (noise_dim, num_angles)
        denom = np.sum(np.abs(un_h_a)**2, axis=0)      # (num_angles,)

        pseudo_spectrum = 1.0 / np.maximum(denom, 1e-12)
        spectrum_db = 10.0 * np.log10(pseudo_spectrum)
        
        peak_angle = float(self.angles_deg[np.argmax(spectrum_db)])
        return self.angles_deg, spectrum_db, peak_angle
