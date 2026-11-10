"""
Deterministic Unit Tests for Synthetic RadarDataset Generator & PyTorch DataLoader
Exercises dataset initialization, random scene generation across all 4 target classes,
Range-Doppler tensor shapes, Gaussian splat heatmap masks, bounding box targets, and batching.
"""
import os
import sys
import unittest
import numpy as np
import torch
from torch.utils.data import DataLoader

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sim.radar_config import RadarConfig
from src.models.radar_dataset import RadarDataset, CLASS_MAP, NUM_CLASSES

class TestRadarDataset(unittest.TestCase):

    def setUp(self):
        # Use compact radar config for fast test execution (<0.5s)
        self.fast_config = RadarConfig(
            num_samples=32,
            num_chirps=16,
            num_rx=2,
            sampling_rate=5e6,
            chirp_duration=20e-6,
            bandwidth=100e6
        )

    def test_dataset_initialization_and_len(self):
        """Verifies default and custom initialization, and __len__."""
        ds_default = RadarDataset(num_samples=10)
        self.assertEqual(len(ds_default), 10)
        self.assertIsNotNone(ds_default.config)

        ds_custom = RadarDataset(num_samples=25, config=self.fast_config, seed=42)
        self.assertEqual(len(ds_custom), 25)
        self.assertEqual(ds_custom.config.num_samples, 32)

    def test_generate_random_scene_all_classes(self):
        """Exercises _generate_random_scene across multiple seeds to hit all 4 target classes."""
        ds = RadarDataset(num_samples=50, config=self.fast_config)
        
        seen_classes = set()
        for idx in range(30):
            targets, snr = ds._generate_random_scene(idx)
            self.assertGreaterEqual(len(targets), 1)
            self.assertLessEqual(len(targets), 4)
            self.assertGreaterEqual(snr, 10.0)
            self.assertLessEqual(snr, 25.0)

            for target in targets:
                seen_classes.add(target.label)
                self.assertIn(target.label, CLASS_MAP)
                # Verify physical kinematic boundaries
                self.assertGreater(target.range_m, 0.0)
                self.assertTrue(np.isfinite(target.velocity_mps))
                self.assertTrue(np.isfinite(target.azimuth_deg))

        # Assert all 4 target categories were generated
        expected_classes = {"car", "pedestrian", "cyclist", "drone"}
        self.assertTrue(expected_classes.issubset(seen_classes), f"Missing classes: {expected_classes - seen_classes}")

    def test_getitem_shapes_and_normalization(self):
        """Verifies __getitem__ tensor shapes, dtypes, and [0, 1] normalization."""
        ds = RadarDataset(num_samples=5, config=self.fast_config, seed=77)
        rdm_tensor, heatmap_target, box_target = ds[0]

        # rdm_tensor: (1, num_doppler, num_range)
        self.assertIsInstance(rdm_tensor, torch.Tensor)
        self.assertEqual(rdm_tensor.dtype, torch.float32)
        self.assertEqual(rdm_tensor.shape, (1, self.fast_config.num_chirps, self.fast_config.num_samples))
        # Value bounds in [0, 1]
        self.assertGreaterEqual(float(torch.min(rdm_tensor)), 0.0)
        self.assertLessEqual(float(torch.max(rdm_tensor)), 1.0)

        # heatmap_target: (NUM_CLASSES, num_doppler, num_range)
        self.assertIsInstance(heatmap_target, torch.Tensor)
        self.assertEqual(heatmap_target.dtype, torch.float32)
        self.assertEqual(heatmap_target.shape, (NUM_CLASSES, self.fast_config.num_chirps, self.fast_config.num_samples))
        # Background class should have non-zero presence
        self.assertGreater(float(torch.mean(heatmap_target[0])), 0.5)

        # box_target: (4, num_doppler, num_range)
        self.assertIsInstance(box_target, torch.Tensor)
        self.assertEqual(box_target.dtype, torch.float32)
        self.assertEqual(box_target.shape, (4, self.fast_config.num_chirps, self.fast_config.num_samples))

    def test_dataloader_batching(self):
        """Verifies PyTorch DataLoader integration with batching and shuffling."""
        ds = RadarDataset(num_samples=8, config=self.fast_config, seed=99)
        loader = DataLoader(ds, batch_size=4, shuffle=True)

        batches = list(loader)
        self.assertEqual(len(batches), 2)

        batch_rdm, batch_heatmap, batch_box = batches[0]
        self.assertEqual(batch_rdm.shape, (4, 1, self.fast_config.num_chirps, self.fast_config.num_samples))
        self.assertEqual(batch_heatmap.shape, (4, NUM_CLASSES, self.fast_config.num_chirps, self.fast_config.num_samples))
        self.assertEqual(batch_box.shape, (4, 4, self.fast_config.num_chirps, self.fast_config.num_samples))

if __name__ == "__main__":
    unittest.main()
