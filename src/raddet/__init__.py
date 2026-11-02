"""
src/raddet — RadDet Radar Spectrum Detection & Wideband Benchmark Package.
"""

from src.raddet.config import (
    RADDET_CLASSES,
    CLASS_COLORS,
    DEFAULT_CONFIG
)
from src.raddet.dataset import (
    load_yolo_annotations,
    denormalize_boxes,
    normalize_boxes,
    RadDetDataset
)
from src.raddet.visualize import (
    plot_spectrogram_detections
)

__all__ = [
    "RADDET_CLASSES",
    "CLASS_COLORS",
    "DEFAULT_CONFIG",
    "load_yolo_annotations",
    "denormalize_boxes",
    "normalize_boxes",
    "RadDetDataset",
    "plot_spectrogram_detections"
]

