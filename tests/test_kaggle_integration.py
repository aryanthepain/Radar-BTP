"""Unit tests for Kaggle Integration & Telemetry Standards."""

import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.push_kaggle_kernel import build_and_push_kernel, validate_notebook
from src.telemetry import StageProgressTracker, format_duration


class TestKaggleTelemetry(unittest.TestCase):
    """Test suite for in-container telemetry tracker and ETC formatting."""

    def test_format_duration(self):
        self.assertEqual(format_duration(0), "00m 00s")
        self.assertEqual(format_duration(45), "00m 45s")
        self.assertEqual(format_duration(125), "02m 05s")
        self.assertEqual(format_duration(3665), "01h 01m 05s")

    def test_stage_progress_tracker_output(self):
        tracker = StageProgressTracker(
            stage_name="Training",
            total_items=100,
            stage_idx=1,
            total_stages=3,
        )
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            tracker.update(step_items=25, extra_info="Loss: 0.42")
            tracker.finish()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("[STAGE 1/3: TRAINING]", output)
        self.assertIn("25/100 ( 25.0%)", output)
        self.assertIn("Stage ETC:", output)
        self.assertIn("Loss: 0.42", output)
        self.assertIn("[SUCCESS]", output)
        self.assertIn("Completed in", output)


class TestKaggleKernelBuilder(unittest.TestCase):
    """Test suite for Kaggle kernel validation and metadata generator."""

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.test_dir.name)

        # Create a valid minimal synthetic notebook
        self.sample_nb = self.temp_path / "sample_notebook.ipynb"
        nb_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# Test Kaggle Notebook"],
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["import torch\n", "print(torch.__version__)\n"],
                },
            ],
            "metadata": {
                "language_info": {"name": "python"},
            },
            "nbformat": 4,
            "nbformat_minor": 4,
        }
        with open(self.sample_nb, "w", encoding="utf-8") as f:
            json.dump(nb_content, f)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_validate_notebook_valid(self):
        nb_data = validate_notebook(self.sample_nb)
        self.assertEqual(len(nb_data["cells"]), 2)

    def test_validate_notebook_empty(self):
        empty_nb = self.temp_path / "empty.ipynb"
        with open(empty_nb, "w", encoding="utf-8") as f:
            json.dump({"cells": []}, f)
        with self.assertRaises(ValueError):
            validate_notebook(empty_nb)

    def test_build_kernel_staging(self):
        build_dir = self.temp_path / "build"
        target_dir = build_and_push_kernel(
            notebook_path=self.sample_nb,
            title="Sample Test Kernel",
            slug="sample-test-kernel",
            username="testuser",
            datasets=["abcxyzi/raddet-icassp-2025"],
            enable_gpu=True,
            enable_internet=False,
            is_private=True,
            push=False,
            build_dir=build_dir,
        )

        metadata_file = target_dir / "kernel-metadata.json"
        self.assertTrue(metadata_file.is_file())

        with open(metadata_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.assertEqual(meta["id"], "testuser/sample-test-kernel")
        self.assertEqual(meta["code_file"], "sample_notebook.ipynb")
        self.assertEqual(meta["dataset_sources"], ["abcxyzi/raddet-icassp-2025"])
        self.assertEqual(meta["enable_gpu"], "true")
        self.assertEqual(meta["enable_internet"], "false")
        self.assertEqual(meta["is_private"], "true")


if __name__ == "__main__":
    unittest.main()
