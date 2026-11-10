"""
Deterministic Smoke Tests for CLI Pipeline Runners, Kaggle Kernel Packaging, and Utility Scripts
Exercises scripts/push_kaggle_kernel.py, src/telemetry.py, radar target scenarios, and detector loss branches.
"""
import os
import sys
import json
import unittest
import tempfile
from pathlib import Path
import numpy as np
import torch

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sim.radar_config import RadarConfig
from src.sim.target import create_standard_traffic_scenario
from src.telemetry import format_duration, StageProgressTracker
from src.models.radar_detector_cnn import RadarObjectDetectorCNN
from scripts.push_kaggle_kernel import get_default_username, validate_notebook, build_parser

class TestPipelineScripts(unittest.TestCase):

    def test_telemetry_format_duration_and_tracker(self):
        """Exercises format_duration with hours and minutes, and tracker with total_items=None."""
        self.assertEqual(format_duration(0), "00m 00s")
        self.assertEqual(format_duration(65), "01m 05s")
        self.assertEqual(format_duration(3665), "01h 01m 05s")
        self.assertEqual(format_duration(7200), "02h 00m 00s")

        # Test tracker without total_items
        tracker = StageProgressTracker(stage_name="unbounded_stage", total_items=None)
        tracker.update(step_items=5, extra_info="testing unbounded")
        tracker.finish()

    def test_radar_config_and_target_scenario(self):
        """Exercises unused properties in RadarConfig and create_standard_traffic_scenario."""
        cfg = RadarConfig()
        self.assertGreater(cfg.max_unambiguous_velocity, 0.0)
        self.assertGreater(cfg.frame_duration, 0.0)
        angle_axis = cfg.get_angle_axis(num_angle_bins=90)
        self.assertEqual(len(angle_axis), 90)
        self.assertAlmostEqual(angle_axis[0], -90.0)
        self.assertAlmostEqual(angle_axis[-1], 90.0)

        targets = create_standard_traffic_scenario()
        self.assertEqual(len(targets), 4)
        labels = [t.label for t in targets]
        self.assertIn("car", labels)
        self.assertIn("pedestrian", labels)
        self.assertIn("cyclist", labels)

    def test_detector_loss_foreground_branch(self):
        """Verifies RadarObjectDetectorCNN compute_loss with active foreground mask (line 105)."""
        detector = RadarObjectDetectorCNN(in_channels=1, num_classes=5)
        cls_logits = torch.randn(2, 5, 32, 32)
        box_preds = torch.randn(2, 4, 32, 32)

        # Create target heatmaps with strong foreground peak
        heatmap_targets = torch.zeros(2, 5, 32, 32)
        heatmap_targets[:, 1, 10, 10] = 1.0  # foreground class > 0.3
        box_targets = torch.zeros(2, 4, 32, 32)
        box_targets[:, :, 10, 10] = 0.5

        total_loss, cls_loss, box_loss = detector.compute_loss(
            cls_logits, box_preds, heatmap_targets, box_targets
        )
        self.assertGreater(float(box_loss), 0.0)
        self.assertGreater(float(total_loss), 0.0)

    def test_kaggle_kernel_builder_utilities(self):
        """Exercises push_kaggle_kernel.py utilities (get_default_username, validate_notebook, parser)."""
        username = get_default_username()
        self.assertIsInstance(username, str)
        self.assertTrue(len(username) > 0)

        # Build and check CLI argument parser
        parser = build_parser()
        args = parser.parse_args(["--notebook", "notebooks/01_radar_classical_dsp.ipynb", "--slug", "test-slug"])
        self.assertEqual(args.notebook, Path("notebooks/01_radar_classical_dsp.ipynb"))
        self.assertEqual(args.slug, "test-slug")
        self.assertFalse(args.push)

        # Test valid notebook validation
        with tempfile.TemporaryDirectory() as tmpdir:
            nb_file = Path(tmpdir) / "test.ipynb"
            with open(nb_file, "w", encoding="utf-8") as f:
                json.dump({"cells": [{"cell_type": "code", "source": ["print(1)"]}]}, f)

            nb_data = validate_notebook(nb_file)
            self.assertEqual(len(nb_data["cells"]), 1)

            # Test empty cells validation error
            nb_empty = Path(tmpdir) / "empty.ipynb"
            with open(nb_empty, "w", encoding="utf-8") as f:
                json.dump({"cells": []}, f)
            with self.assertRaises(ValueError):
                validate_notebook(nb_empty)

            # Test invalid JSON validation error
            nb_invalid = Path(tmpdir) / "invalid.ipynb"
            with open(nb_invalid, "w", encoding="utf-8") as f:
                f.write("not json")
            with self.assertRaises(ValueError):
                validate_notebook(nb_invalid)

            # Test non-existent file
            with self.assertRaises(FileNotFoundError):
                validate_notebook(Path(tmpdir) / "nonexistent.ipynb")

if __name__ == "__main__":
    unittest.main()
