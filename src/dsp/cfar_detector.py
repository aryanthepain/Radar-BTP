"""
Constant False Alarm Rate (CFAR) Target Detectors (2D & 1D)
Implements CA-CFAR (Cell Averaging), OS-CFAR (Ordered Statistic), and GOCA/SOCA-CFAR.
"""
from typing import List, Dict, Tuple, Optional, Literal
import numpy as np

class CFARDetector2D:
    """
    2D Adaptive Threshold CFAR Detector on Range-Doppler Matrices.
    """

    def __init__(
        self,
        num_train_range: int = 4,
        num_train_doppler: int = 4,
        num_guard_range: int = 2,
        num_guard_doppler: int = 2,
        p_fa: float = 1e-4,
        cfar_type: Literal["ca", "os", "goca", "soca"] = "ca",
        os_rank_k: Optional[int] = None
    ):
        self.num_train_r = num_train_range
        self.num_train_d = num_train_doppler
        self.num_guard_r = num_guard_range
        self.num_guard_d = num_guard_doppler
        self.p_fa = p_fa
        self.cfar_type = cfar_type

        # Total window half-dimensions
        self.win_r = self.num_train_r + self.num_guard_r
        self.win_d = self.num_train_d + self.num_guard_d

        # Number of training cells
        total_cells = (2 * self.win_r + 1) * (2 * self.win_d + 1)
        guard_cells = (2 * self.num_guard_r + 1) * (2 * self.num_guard_d + 1)
        self.n_train = total_cells - guard_cells

        # Default OS-CFAR rank k (typically 75th percentile of training cells)
        self.os_rank_k = os_rank_k or int(0.75 * self.n_train)

        # Theoretical threshold factor alpha for CA-CFAR in Rayleigh noise
        # P_fa = (1 + alpha / N)^(-N)  =>  alpha = N * (P_fa^(-1/N) - 1)
        if self.n_train > 0:
            self.alpha_ca = self.n_train * (self.p_fa ** (-1.0 / self.n_train) - 1.0)
        else:
            self.alpha_ca = 1.0

    def detect(
        self,
        rdm_power: np.ndarray,
        range_axis: Optional[np.ndarray] = None,
        velocity_axis: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, np.ndarray, List[Dict[str, float]]]:
        """
        Executes CFAR detection over 2D power map (linear scale).
        
        Args:
            rdm_power: 2D array of power values (shape: num_doppler, num_range).
            range_axis: Optional 1D range axis (meters).
            velocity_axis: Optional 1D velocity axis (m/s).
            
        Returns:
            detection_mask: 2D boolean array (True where target is detected).
            threshold_map: 2D array of computed adaptive noise threshold levels.
            detections: List of detection dictionaries with indices, range, velocity, and power.
        """
        # Ensure power is in linear scale
        power = np.copy(rdm_power)
        n_d, n_r = power.shape

        threshold_map = np.zeros_like(power)
        detection_mask = np.zeros_like(power, dtype=bool)
        detections = []

        wr, wd = self.win_r, self.win_d
        gr, gd = self.num_guard_r, self.num_guard_d

        # Slide CUT (Cell Under Test) across the 2D grid
        for i in range(wd, n_d - wd):
            for j in range(wr, n_r - wr):
                cut_val = power[i, j]

                # Full outer window
                full_win = power[i - wd : i + wd + 1, j - wr : j + wr + 1]
                
                # Guard window
                guard_win = power[i - gd : i + gd + 1, j - gr : j + gr + 1]
                
                if self.cfar_type == "ca":
                    # Cell-Averaging: Sum(full) - Sum(guard)
                    train_sum = np.sum(full_win) - np.sum(guard_win)
                    noise_est = train_sum / self.n_train
                    thresh = self.alpha_ca * noise_est

                elif self.cfar_type == "os":
                    # Ordered-Statistic: Extract non-guard cells and sort
                    mask = np.ones(full_win.shape, dtype=bool)
                    mask[wd - gd : wd + gd + 1, wr - gr : wr + gr + 1] = False
                    training_samples = full_win[mask]
                    sorted_samples = np.sort(training_samples)
                    k_idx = min(self.os_rank_k, len(sorted_samples) - 1)
                    noise_est = sorted_samples[k_idx]
                    thresh = self.alpha_ca * noise_est

                elif self.cfar_type == "goca":
                    # Greatest-Of: Max of leading and lagging Doppler halves
                    lead_win = power[i - wd : i - gd, j - wr : j + wr + 1]
                    lag_win = power[i + gd + 1 : i + wd + 1, j - wr : j + wr + 1]
                    mean_lead = np.mean(lead_win) if lead_win.size > 0 else 0.0
                    mean_lag = np.mean(lag_win) if lag_win.size > 0 else 0.0
                    noise_est = max(mean_lead, mean_lag)
                    thresh = self.alpha_ca * noise_est

                elif self.cfar_type == "soca":
                    # Smallest-Of: Min of leading and lagging Doppler halves
                    lead_win = power[i - wd : i - gd, j - wr : j + wr + 1]
                    lag_win = power[i + gd + 1 : i + wd + 1, j - wr : j + wr + 1]
                    mean_lead = np.mean(lead_win) if lead_win.size > 0 else 1e-12
                    mean_lag = np.mean(lag_win) if lag_win.size > 0 else 1e-12
                    noise_est = min(mean_lead, mean_lag)
                    thresh = self.alpha_ca * noise_est

                else:
                    train_sum = np.sum(full_win) - np.sum(guard_win)
                    noise_est = train_sum / self.n_train
                    thresh = self.alpha_ca * noise_est

                threshold_map[i, j] = thresh

                # Check if CUT exceeds threshold
                if cut_val > thresh:
                    # Also enforce local peak check (3x3 local maximum)
                    local_3x3 = power[i-1:i+2, j-1:j+2]
                    if cut_val >= np.max(local_3x3):
                        detection_mask[i, j] = True
                        r_val = range_axis[j] if range_axis is not None else float(j)
                        v_val = velocity_axis[i] if velocity_axis is not None else float(i)
                        snr_est = 10.0 * np.log10(max(cut_val / max(noise_est, 1e-12), 1.0))
                        detections.append({
                            "range_bin": j,
                            "doppler_bin": i,
                            "range_m": float(r_val),
                            "velocity_mps": float(v_val),
                            "peak_power": float(cut_val),
                            "snr_db": float(snr_est)
                        })

        return detection_mask, threshold_map, detections
