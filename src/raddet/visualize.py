"""
visualize.py — Publication-grade Cyber-Radar spectrogram and detection visualizer.

Provides high-contrast bounding box overlays, confidence score annotations,
and side-by-side ground truth vs prediction figures for RadDet spectrum detection.
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Safe headless rendering invariant
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from src.raddet.config import CLASS_COLORS, RADDET_CLASSES
from src.raddet.dataset import denormalize_boxes


def plot_spectrogram_detections(
    spectrogram: Union[np.ndarray, "torch.Tensor"],
    gt_boxes: Optional[Union[List, np.ndarray]] = None,
    pred_boxes: Optional[Union[List, np.ndarray]] = None,
    class_names: Optional[Dict[int, str]] = None,
    title: Optional[str] = "RadDet Radar Spectrum Detection",
    ax: Optional[plt.Axes] = None,
    normalized: bool = True
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Render a high-contrast Cyber-Radar spectrogram with bounding box annotations.
    
    Args:
        spectrogram: 2D array (H, W) or (1, H, W) normalized to [0, 1] or [0, 255].
        gt_boxes: List or array of ground-truth annotations:
                  - if normalized: list of [cls_id, x_c, y_c, w, h] or dicts
                  - or pixel [cls_id, x1, y1, x2, y2]
        pred_boxes: List or array of prediction annotations:
                    - [cls_id, conf, x_c, y_c, w, h] or [cls_id, conf, x1, y1, x2, y2]
        class_names: Dict mapping class_id -> name. Defaults to RADDET_CLASSES.
        title: Plot title.
        ax: Matplotlib Axes object. If None, a new figure is created.
        normalized: Whether box coordinates are normalized in [0, 1].
        
    Returns:
        (fig, ax)
    """
    if class_names is None:
        class_names = RADDET_CLASSES
        
    # Handle tensor or array input
    if hasattr(spectrogram, "detach"):
        spec_np = spectrogram.detach().cpu().numpy()
    else:
        spec_np = np.asarray(spectrogram)
        
    if spec_np.ndim == 3 and spec_np.shape[0] in (1, 3):
        spec_np = spec_np[0]
        
    h, w = spec_np.shape[:2]
    
    # Create plot if ax is None
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6), facecolor="#0a0e17")
    else:
        fig = ax.figure
        
    ax.set_facecolor("#0a0e17")
    
    # Render spectrogram with cyber-radar colormap (viridis / inferno / plasma)
    im = ax.imshow(
        spec_np,
        cmap="magma",
        aspect="auto",
        origin="lower",
        extent=[0, w, 0, h]
    )
    
    # Draw Ground Truth Boxes (Cyan / White outline)
    if gt_boxes is not None and len(gt_boxes) > 0:
        for box in gt_boxes:
            if isinstance(box, dict):
                cls_id = int(box["class_id"])
                coords = [box["x_c"], box["y_c"], box["w"], box["h"]]
            else:
                cls_id = int(box[0])
                coords = box[1:]
                
            if normalized:
                pts = denormalize_boxes([coords[:4]], w, h)[0]
            else:
                pts = coords[:4]
                
            x1, y1, x2, y2 = pts
            bw = x2 - x1
            bh = y2 - y1
            
            c_name = class_names.get(cls_id, f"Class {cls_id}")
            box_color = CLASS_COLORS.get(cls_id, "#00FFCC")
            
            rect = patches.Rectangle(
                (x1, y1), bw, bh,
                linewidth=1.8,
                edgecolor=box_color,
                facecolor="none",
                linestyle="--",
                alpha=0.9
            )
            ax.add_patch(rect)
            ax.text(
                x1, y2 + 1,
                f"GT: {c_name}",
                color=box_color,
                fontsize=8,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#0a0e17", edgecolor=box_color, alpha=0.7)
            )
            
    # Draw Prediction Boxes (Solid vibrant outline with confidence tag)
    if pred_boxes is not None and len(pred_boxes) > 0:
        for pbox in pred_boxes:
            if isinstance(pbox, dict):
                cls_id = int(pbox["class_id"])
                conf = float(pbox.get("conf", 1.0))
                coords = [pbox["x_c"], pbox["y_c"], pbox["w"], pbox["h"]]
            else:
                cls_id = int(pbox[0])
                conf = float(pbox[1])
                coords = pbox[2:]
                
            if normalized:
                pts = denormalize_boxes([coords[:4]], w, h)[0]
            else:
                pts = coords[:4]
                
            x1, y1, x2, y2 = pts
            bw = x2 - x1
            bh = y2 - y1
            
            c_name = class_names.get(cls_id, f"Class {cls_id}")
            pred_color = "#76FF03" if conf > 0.5 else "#FF9100"
            
            rect = patches.Rectangle(
                (x1, y1), bw, bh,
                linewidth=2.2,
                edgecolor=pred_color,
                facecolor="none",
                alpha=0.95
            )
            ax.add_patch(rect)
            ax.text(
                x1, y1 - 4,
                f"{c_name} {conf:.2f}",
                color=pred_color,
                fontsize=8,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#0a0e17", edgecolor=pred_color, alpha=0.85)
            )
            
    ax.set_title(title, color="#E0E6ED", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Time Dwell (samples)", color="#8C9EAE", fontsize=9)
    ax.set_ylabel("Frequency Channel (MHz)", color="#8C9EAE", fontsize=9)
    ax.tick_params(colors="#8C9EAE", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#2D3748")
        
    return fig, ax

