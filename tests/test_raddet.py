"""
test_raddet.py — Deterministic unit tests for RadDet spectrum detection module.

Covers:
1. ICASSP 2025 class mapping and configurations.
2. Forward and inverse coordinate bounding box conversions.
3. PyTorch RadDetDataset loading and tensor shapes.
4. Spectrogram detection visualizer smoke tests.
5. PyTorch Conv2d layer forward pass with RadDet tensors.
"""

import os
import unittest
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn

# Set non-interactive matplotlib backend and writable config dir
os.environ["MPLCONFIGDIR"] = os.path.join(os.getcwd(), ".tmp_mpl")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.raddet.config import RADDET_CLASSES, CLASS_COLORS, DEFAULT_CONFIG
from src.raddet.dataset import (
    load_yolo_annotations,
    denormalize_boxes,
    normalize_boxes,
    RadDetDataset
)
from src.raddet.visualize import plot_spectrogram_detections


class TestRadDetModule(unittest.TestCase):
    """Test suite for RadDet radar spectrum detection dataset & utilities."""

    def test_class_mapping(self):
        """Verify the 11 ICASSP 2025 radar modulation classes and color bindings."""
        self.assertEqual(len(RADDET_CLASSES), 11)
        expected_classes = [
            "Rect", "Barker", "Frank", "P1", "P2",
            "P3", "P4", "Px", "ZadoffChu", "LFM", "FMCW"
        ]
        for idx, name in enumerate(expected_classes):
            self.assertEqual(RADDET_CLASSES[idx], name)
            self.assertIn(idx, CLASS_COLORS)
            
        self.assertEqual(DEFAULT_CONFIG["num_classes"], 11)
        self.assertEqual(DEFAULT_CONFIG["default_resolution"], (128, 128))

    def test_box_normalization_roundtrip(self):
        """Verify coordinate normalization and denormalization round-trip within 1e-5."""
        w, h = 128, 128
        # Create arbitrary normalized boxes [x_c, y_c, w_norm, h_norm]
        orig_norm = np.array([
            [0.50, 0.50, 0.20, 0.30],
            [0.25, 0.75, 0.15, 0.10],
            [0.80, 0.20, 0.10, 0.25]
        ], dtype=np.float32)

        pixel_boxes = denormalize_boxes(orig_norm, width=w, height=h)
        self.assertEqual(pixel_boxes.shape, (3, 4))
        
        # Verify box [0]: center (64, 64), width 25.6, height 38.4
        self.assertAlmostEqual(pixel_boxes[0, 0], 64.0 - 12.8, places=4)
        self.assertAlmostEqual(pixel_boxes[0, 2], 64.0 + 12.8, places=4)
        self.assertAlmostEqual(pixel_boxes[0, 1], 64.0 - 19.2, places=4)
        self.assertAlmostEqual(pixel_boxes[0, 3], 64.0 + 19.2, places=4)

        # Invert back to normalized
        reconstructed_norm = normalize_boxes(pixel_boxes, width=w, height=h)
        np.testing.assert_allclose(orig_norm, reconstructed_norm, atol=1e-5)

    def test_dataset_loading(self):
        """Verify RadDetDataset loads sample images and parses YOLO annotations."""
        sample_dir = Path("data/raddet_sample")
        if not sample_dir.exists():
            from scripts.fetch_raddet_sample import populate_dataset
            populate_dataset(sample_dir)

        dataset = RadDetDataset(root_dir=sample_dir, split="train")
        self.assertGreaterEqual(len(dataset), 40)

        # Inspect first item
        img_tensor, targets = dataset[0]
        self.assertIsInstance(img_tensor, torch.Tensor)
        self.assertEqual(img_tensor.shape, (1, 128, 128))
        self.assertEqual(img_tensor.dtype, torch.float32)
        self.assertGreaterEqual(img_tensor.min().item(), 0.0)
        self.assertLessEqual(img_tensor.max().item(), 1.0)

        # Inspect targets dict
        self.assertIn("boxes", targets)
        self.assertIn("labels", targets)
        self.assertIn("image_id", targets)
        self.assertGreater(len(targets["boxes"]), 0)
        self.assertEqual(targets["boxes"].shape[1], 4)
        self.assertEqual(targets["labels"].shape[0], targets["boxes"].shape[0])

    def test_visualizer_smoke(self):
        """Verify plot_spectrogram_detections renders a figure cleanly with annotations."""
        spectrogram = np.random.uniform(0.0, 1.0, size=(128, 128)).astype(np.float32)
        gt_boxes = [
            {"class_id": 9, "x_c": 0.4, "y_c": 0.5, "w": 0.3, "h": 0.2}
        ]
        pred_boxes = [
            {"class_id": 9, "conf": 0.94, "x_c": 0.41, "y_c": 0.51, "w": 0.29, "h": 0.21}
        ]

        fig, ax = plot_spectrogram_detections(
            spectrogram=spectrogram,
            gt_boxes=gt_boxes,
            pred_boxes=pred_boxes,
            title="Smoke Test Detection"
        )
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)
        plt.close(fig)

    def test_pytorch_conv_forward(self):
        """Verify RadDet spectrogram batch passes through a PyTorch Conv2d block cleanly."""
        batch_size = 4
        # Synthetic batch of RadDet 128x128 spectrogram tensors (B, 1, 128, 128)
        x = torch.randn(batch_size, 1, 128, 128)

        # Simple lightweight feature extraction backbone
        model = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2),  # -> (B, 16, 64, 64)
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),  # -> (B, 32, 1, 1)
            nn.Flatten(),  # -> (B, 32)
            nn.Linear(32, 11)  # 11 RadDet classes
        )

        out = model(x)
        self.assertEqual(out.shape, (batch_size, 11))
        loss = out.sum()
        loss.backward()  # Gradient propagation check
        self.assertIsNotNone(model[0].weight.grad)


if __name__ == "__main__":
    unittest.main()

