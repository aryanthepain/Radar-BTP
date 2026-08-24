"""
Synthetic Radar Dataset Generator and PyTorch Dataset Loader
Generates labeled Range-Doppler heatmaps with ground-truth target bounding boxes and semantic classes.
"""
from typing import Tuple, List, Dict, Optional
import numpy as np
import torch
from torch.utils.data import Dataset
from src.sim.radar_config import RadarConfig
from src.sim.target import RadarTarget
from src.sim.radar_sim import FMCWRadarSimulator
from src.dsp.range_processing import RangeProcessor
from src.dsp.clutter_removal import ClutterFilter
from src.dsp.doppler_processing import DopplerProcessor

CLASS_MAP = {
    "background": 0,
    "car": 1,
    "pedestrian": 2,
    "cyclist": 3,
    "drone": 4
}
NUM_CLASSES = len(CLASS_MAP)

class RadarDataset(Dataset):
    """
    Synthesizes diverse radar scenes on the fly or pre-generates samples for training deep learning radar detectors.
    """

    def __init__(self, num_samples: int = 200, config: Optional[RadarConfig] = None, seed: int = 123):
        self.num_samples = num_samples
        self.config = config or RadarConfig()
        self.sim = FMCWRadarSimulator(self.config)
        self.range_proc = RangeProcessor(self.config)
        self.clutter_filter = ClutterFilter(method="mean_subtraction")
        self.doppler_proc = DopplerProcessor(self.config)
        self.rng = np.random.default_rng(seed)

    def __len__(self) -> int:
        return self.num_samples

    def _generate_random_scene(self, idx: int) -> Tuple[List[RadarTarget], float]:
        """Generates random combination of 1 to 4 targets with random positions and velocities."""
        local_rng = np.random.default_rng(idx + 1000)
        num_targets = local_rng.integers(1, 4)
        targets = []
        classes = ["car", "pedestrian", "cyclist", "drone"]

        for _ in range(num_targets):
            cls = local_rng.choice(classes)
            if cls == "car":
                r = local_rng.uniform(10.0, 35.0)
                v = local_rng.uniform(-20.0, 20.0)
                th = local_rng.uniform(-25.0, 25.0)
                rcs = local_rng.uniform(5.0, 15.0)
                t = RadarTarget(range_m=r, velocity_mps=v, azimuth_deg=th, rcs_dbsm=rcs, label=cls)
            elif cls == "pedestrian":
                r = local_rng.uniform(4.0, 20.0)
                v = local_rng.uniform(-2.5, 2.5)
                th = local_rng.uniform(-35.0, 35.0)
                rcs = local_rng.uniform(-8.0, -1.0)
                t = RadarTarget(range_m=r, velocity_mps=v, azimuth_deg=th, rcs_dbsm=rcs, label=cls, micro_doppler_freq=2.0, micro_doppler_amp=0.5)
            elif cls == "cyclist":
                r = local_rng.uniform(6.0, 25.0)
                v = local_rng.uniform(-8.0, 8.0)
                th = local_rng.uniform(-30.0, 30.0)
                rcs = local_rng.uniform(0.0, 4.0)
                t = RadarTarget(range_m=r, velocity_mps=v, azimuth_deg=th, rcs_dbsm=rcs, label=cls)
            else: # drone
                r = local_rng.uniform(5.0, 30.0)
                v = local_rng.uniform(-10.0, 10.0)
                th = local_rng.uniform(-40.0, 40.0)
                rcs = local_rng.uniform(-12.0, -4.0)
                t = RadarTarget(range_m=r, velocity_mps=v, azimuth_deg=th, rcs_dbsm=rcs, label=cls, micro_doppler_freq=50.0, micro_doppler_amp=1.2)
            targets.append(t)

        snr = local_rng.uniform(10.0, 25.0)
        return targets, snr

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Returns:
            rdm_tensor: (1, num_doppler, num_range) normalized float tensor.
            heatmap_target: (num_classes, num_doppler, num_range) binary/gaussian target mask.
            box_target: (4, num_doppler, num_range) regression target [r_norm, v_norm, width_r, width_v].
        """
        targets, snr = self._generate_random_scene(idx)
        
        # Simulate raw cube
        radar_cube = self.sim.generate_radar_cube(
            targets=targets,
            snr_db=snr,
            clutter_ratio_db=8.0,
            include_clutter=True,
            seed=idx + 500
        )

        # Range FFT -> Clutter Filter -> Doppler FFT
        range_cube, range_axis = self.range_proc.process(radar_cube)
        filtered_cube = self.clutter_filter.filter(range_cube, slow_time_axis=1)
        rdm, velocity_axis, _ = self.doppler_proc.process(filtered_cube)

        # Average power across Rx antennas
        rdm_power = np.mean(np.abs(rdm)**2, axis=0) # (num_doppler, num_range)
        rdm_db = 10.0 * np.log10(np.maximum(rdm_power, 1e-12))
        # Normalize to [0, 1] range
        rdm_norm = (rdm_db - np.min(rdm_db)) / (np.max(rdm_db) - np.min(rdm_db) + 1e-8)

        n_d, n_r = rdm_norm.shape
        heatmap = np.zeros((NUM_CLASSES, n_d, n_r), dtype=np.float32)
        heatmap[0, :, :] = 1.0 # Background channel default
        box_targets = np.zeros((4, n_d, n_r), dtype=np.float32)

        # Populate ground truth target positions
        for target in targets:
            cls_id = CLASS_MAP.get(target.label, 1)
            # Find nearest range and doppler indices
            r_idx = int(np.argmin(np.abs(range_axis - target.range_m)))
            v_idx = int(np.argmin(np.abs(velocity_axis - target.velocity_mps)))

            # Clip within bounds
            r_idx = np.clip(r_idx, 2, n_r - 3)
            v_idx = np.clip(v_idx, 2, n_d - 3)

            # Apply 2D Gaussian splat on target position
            for di in range(-2, 3):
                for dj in range(-2, 3):
                    dist_sq = di**2 + dj**2
                    gaussian_val = np.exp(-dist_sq / 2.0)
                    cur_d = v_idx + di
                    cur_r = r_idx + dj
                    heatmap[cls_id, cur_d, cur_r] = max(heatmap[cls_id, cur_d, cur_r], gaussian_val)
                    heatmap[0, cur_d, cur_r] = min(heatmap[0, cur_d, cur_r], 1.0 - gaussian_val)

                    # Bounding box regression targets
                    box_targets[0, cur_d, cur_r] = target.range_m / self.config.max_unambiguous_range
                    box_targets[1, cur_d, cur_r] = (target.velocity_mps + self.config.max_unambiguous_velocity) / (2 * self.config.max_unambiguous_velocity)
                    box_targets[2, cur_d, cur_r] = 0.05 # default normalized range width
                    box_targets[3, cur_d, cur_r] = 0.05 # default normalized velocity width

        return (
            torch.tensor(rdm_norm, dtype=torch.float32).unsqueeze(0),
            torch.tensor(heatmap, dtype=torch.float32),
            torch.tensor(box_targets, dtype=torch.float32)
        )
