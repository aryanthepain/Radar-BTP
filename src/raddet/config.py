"""
config.py — Configuration parameters, class mappings, and visual themes for RadDet.

Reference: ICASSP 2025 "RadDet: A Wideband Dataset for Real-Time Radar Spectrum Detection"
"""

from typing import Dict, Tuple

# 11 ICASSP 2025 Radar Modulation Classes
RADDET_CLASSES: Dict[int, str] = {
    0: "Rect",
    1: "Barker",
    2: "Frank",
    3: "P1",
    4: "P2",
    5: "P3",
    6: "P4",
    7: "Px",
    8: "ZadoffChu",
    9: "LFM",
    10: "FMCW"
}

# Distinct high-contrast Cyber-Radar color mapping for each class (RGBA / Hex)
CLASS_COLORS: Dict[int, str] = {
    0: "#00FFCC",  # Rect: Cyan
    1: "#00E5FF",  # Barker: Sky Blue
    2: "#3D5AFE",  # Frank: Indigo
    3: "#7C4DFF",  # P1: Deep Purple
    4: "#B388FF",  # P2: Light Purple
    5: "#E040FB",  # P3: Magenta
    6: "#FF4081",  # P4: Pink
    7: "#FF5252",  # Px: Coral Red
    8: "#FF9100",  # ZadoffChu: Orange
    9: "#FFEA00",  # LFM: Yellow
    10: "#76FF03"  # FMCW: Neon Green
}

# Standard RF & STFT Parameters for RadDet-9T-128
DEFAULT_CONFIG = {
    "bandwidth_mhz": 500.0,
    "time_horizon_ms": 2.0,
    "default_resolution": (128, 128),
    "time_resolution_us": 15.6,
    "freq_resolution_mhz": 3.91,
    "num_classes": 11,
}

