"""
tests/test_walkthrough_notebooks.py
Deterministic Unit & Smoke Test Suite for Academic Radar Walkthrough Notebooks
Validates:
  1. Notebook JSON structure, cell counts, and valid nbformat parsing.
  2. Mermaid architecture blocks and collapsible SVG fallback blocks.
  3. Non-empty execution outputs and pre-rendered Matplotlib display_data figures.
  4. Fast deterministic sub-second smoke test of the classical DSP pipeline.
  5. Fast deterministic sub-second smoke test of the PyTorch RadarObjectDetectorCNN.
"""
import os
import sys
from pathlib import Path
import unittest
import numpy as np
import nbformat
import torch

# Ensure repository root is on sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.sim.radar_config import RadarConfig
from src.dsp.range_processing import RangeProcessor
from src.dsp.clutter_removal import ClutterFilter
from src.dsp.doppler_processing import DopplerProcessor
from src.dsp.cfar_detector import CFARDetector2D
from src.dsp.aoa_estimation import AngleEstimator
from src.models.radar_detector_cnn import RadarObjectDetectorCNN
from src.models.radar_dataset import NUM_CLASSES


class TestWalkthroughNotebooks(unittest.TestCase):
    """Deterministic validation of academic walkthrough notebooks and fast algorithmic smoke tests."""

    @classmethod
    def setUpClass(cls):
        cls.nb1_path = os.path.join(ROOT_DIR, "01_radar_classical_dsp.ipynb")
        cls.nb2_path = os.path.join(ROOT_DIR, "02_radar_deep_learning_detection.ipynb")
        cls.nb3_path = os.path.join(ROOT_DIR, "03_raddet_spectrum_detection_kaggle.ipynb")

    def test_01_notebook_files_exist_and_parse(self):
        """Verify that both notebooks exist on disk and parse cleanly via nbformat."""
        self.assertTrue(os.path.exists(self.nb1_path), f"Missing {self.nb1_path}")
        self.assertTrue(os.path.exists(self.nb2_path), f"Missing {self.nb2_path}")

        with open(self.nb1_path, "r", encoding="utf-8") as f:
            nb1 = nbformat.read(f, as_version=4)
        with open(self.nb2_path, "r", encoding="utf-8") as f:
            nb2 = nbformat.read(f, as_version=4)

        self.assertGreaterEqual(len(nb1.cells), 21, "Notebook 01 must contain at least 21 cells.")
        self.assertGreaterEqual(len(nb2.cells), 13, "Notebook 02 must contain at least 13 cells.")

    def test_02_notebook_mermaid_and_fallback_blocks(self):
        """Verify that required Mermaid code blocks and collapsible SVG details are present."""
        with open(self.nb1_path, "r", encoding="utf-8") as f:
            nb1 = nbformat.read(f, as_version=4)
        with open(self.nb2_path, "r", encoding="utf-8") as f:
            nb2 = nbformat.read(f, as_version=4)

        text_1 = "".join("".join(c.get("source", [])) for c in nb1.cells)
        text_2 = "".join("".join(c.get("source", [])) for c in nb2.cells)

        # Notebook 1 checks (11 diagrams expected)
        self.assertGreaterEqual(text_1.count("```mermaid"), 11, "Notebook 01 must have >= 11 Mermaid diagrams.")
        self.assertGreaterEqual(text_1.count("<details>"), 11, "Notebook 01 must have >= 11 collapsible SVG fallbacks.")
        self.assertIn("RangeProcessor.process", text_1)
        self.assertIn("ClutterFilter.filter", text_1)
        self.assertIn("DopplerProcessor.process", text_1)
        self.assertIn("CFARDetector2D.detect", text_1)
        self.assertIn("estimate_aoa_music", text_1)

        # Notebook 2 checks (6 diagrams expected)
        self.assertGreaterEqual(text_2.count("```mermaid"), 6, "Notebook 02 must have >= 6 Mermaid diagrams.")
        self.assertGreaterEqual(text_2.count("<details>"), 6, "Notebook 02 must have >= 6 collapsible SVG fallbacks.")
        self.assertIn("RadarObjectDetectorCNN", text_2)
        self.assertIn("Multi-Task Loss", text_2)
        self.assertIn("Classification Head", text_2)
        self.assertIn("Bounding Box Head", text_2)

    def test_03_notebook_prerendered_outputs(self):
        """Verify that code cells have non-empty execution outputs and figures pre-rendered."""
        with open(self.nb1_path, "r", encoding="utf-8") as f:
            nb1 = nbformat.read(f, as_version=4)
        with open(self.nb2_path, "r", encoding="utf-8") as f:
            nb2 = nbformat.read(f, as_version=4)

        # Check code cell outputs in Notebook 1
        code_cells_1 = [c for c in nb1.cells if c.cell_type == "code"]
        self.assertGreaterEqual(len(code_cells_1), 8)
        has_display_data_1 = False
        for c in code_cells_1:
            self.assertTrue(len(c.outputs) > 0, "All code cells in NB1 must contain pre-rendered outputs.")
            for out in c.outputs:
                if out.output_type == "display_data" and "image/png" in out.data:
                    has_display_data_1 = True
        self.assertTrue(has_display_data_1, "Notebook 01 must contain pre-rendered display_data PNG figures.")

        # Check code cell outputs in Notebook 2
        code_cells_2 = [c for c in nb2.cells if c.cell_type == "code"]
        self.assertGreaterEqual(len(code_cells_2), 5)
        has_display_data_2 = False
        for c in code_cells_2:
            self.assertTrue(len(c.outputs) > 0, "All code cells in NB2 must contain pre-rendered outputs.")
            for out in c.outputs:
                if out.output_type == "display_data" and "image/png" in out.data:
                    has_display_data_2 = True
        self.assertTrue(has_display_data_2, "Notebook 02 must contain pre-rendered display_data PNG figures.")

    def test_04_fast_dsp_pipeline_smoke(self):
        """Execute a sub-second smoke test of the core DSP pipeline on a small dummy 3D radar cube."""
        cfg = RadarConfig(
            fc=77e9,
            bandwidth=1.0e9,
            chirp_duration=50e-6,
            num_samples=64,
            num_chirps=16,
            num_rx=4,
            rx_spacing_factor=0.5,
            sampling_rate=5.12e6
        )

        # Small dummy radar cube: (4 Rx, 16 Chirps, 64 Samples)
        rng = np.random.default_rng(42)
        cube = (rng.standard_normal((4, 16, 64)) + 1j * rng.standard_normal((4, 16, 64))).astype(np.complex64)

        # 1. Range FFT
        range_proc = RangeProcessor(cfg, window="hann")
        range_cube, range_axis = range_proc.process(cube)
        self.assertEqual(range_cube.shape, (4, 16, 64))
        self.assertEqual(len(range_axis), 64)

        # 2. MTI Filter
        mti = ClutterFilter(method="mean_subtraction")
        filtered_cube = mti.filter(range_cube, slow_time_axis=1)
        self.assertEqual(filtered_cube.shape, (4, 16, 64))

        # 3. Doppler FFT
        doppler_proc = DopplerProcessor(cfg, window="hann")
        rdm, vel_axis, _ = doppler_proc.process(filtered_cube)
        self.assertEqual(rdm.shape, (4, 16, 64))
        self.assertEqual(len(vel_axis), 16)

        # 4. 2D CA-CFAR
        cfar = CFARDetector2D(
            num_train_range=2,
            num_train_doppler=2,
            num_guard_range=1,
            num_guard_doppler=1,
            p_fa=1e-3,
            cfar_type="ca"
        )
        rdm_power = np.mean(np.abs(rdm)**2, axis=0)
        det_mask, thresh_map, detections = cfar.detect(rdm_power, range_axis, vel_axis)
        self.assertEqual(det_mask.shape, (16, 64))
        self.assertEqual(thresh_map.shape, (16, 64))
        self.assertIsInstance(detections, list)

        # 5. Spatial AoA (MUSIC)
        aoa_est = AngleEstimator(cfg)
        test_snapshot = rdm[:, 0, 0] # 4 antenna samples
        angles_deg, pseudo_spec, peak_angle = aoa_est.estimate_aoa_music(test_snapshot)
        self.assertEqual(len(angles_deg), 180)
        self.assertGreaterEqual(peak_angle, -90.0)
        self.assertLessEqual(peak_angle, 90.0)

    def test_05_fast_cnn_forward_smoke(self):
        """Execute a sub-second forward pass of RadarObjectDetectorCNN with dummy tensor."""
        model = RadarObjectDetectorCNN(in_channels=1, num_classes=NUM_CLASSES, base_filters=16)
        model.eval()

        dummy_x = torch.randn(2, 1, 128, 129)
        with torch.no_grad():
            cls_out, box_out = model(dummy_x)

        # Expected shape: (batch_size, num_classes, H, W) and (batch_size, 4, H, W)
        self.assertEqual(cls_out.shape, (2, 5, 128, 129))
        self.assertEqual(box_out.shape, (2, 4, 128, 129))

    def test_06_raddet_kaggle_notebook_structure(self):
        """Verify 03_raddet_spectrum_detection_kaggle.ipynb structure, telemetry, and dual paths."""
        self.assertTrue(os.path.exists(self.nb3_path), f"Missing {self.nb3_path}")

        with open(self.nb3_path, "r", encoding="utf-8") as f:
            nb3 = nbformat.read(f, as_version=4)

        self.assertGreaterEqual(len(nb3.cells), 10, "Notebook 03 must contain at least 10 cells.")

        all_text = "".join("".join(c.get("source", [])) for c in nb3.cells)
        code_text = "".join("".join(c.get("source", [])) for c in nb3.cells if c.cell_type == "code")

        # Telemetry verification
        self.assertIn("StageProgressTracker", code_text, "Notebook 03 must embed StageProgressTracker.")
        self.assertIn("ETC:", code_text, "StageProgressTracker must log ETC.")

        # Dual-path abstraction verification
        self.assertIn("/kaggle/input", code_text, "Notebook 03 must handle /kaggle/input.")
        self.assertIn("/kaggle/working", code_text, "Notebook 03 must handle /kaggle/working.")

        # Section coverage
        self.assertIn("Executive Summary", all_text)
        self.assertIn("Environment Setup", all_text)
        self.assertIn("Dataset Ingestion", all_text)
        self.assertIn("YOLO", all_text)
        self.assertIn("Validation & Loss Curves", all_text)
        self.assertIn("Inference & Detection Overlays", all_text)

        # Validate with push_kaggle_kernel validation routine
        from scripts.push_kaggle_kernel import validate_notebook
        validate_notebook(Path(self.nb3_path))


if __name__ == "__main__":
    unittest.main()
