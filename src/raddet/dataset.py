"""
dataset.py — RadDet Dataset Loader, YOLO Label Parser, and Coordinate Transforms.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import torch
from torch.utils.data import Dataset
from PIL import Image

from src.raddet.config import RADDET_CLASSES


def load_yolo_annotations(txt_path: Union[str, Path]) -> List[Dict[str, Union[int, float]]]:
    """
    Parse a YOLO format annotation file.
    
    Each line format:
        <class_id> <x_center> <y_center> <width> <height>
    where coordinates are floats normalized to [0, 1].
    
    Returns:
        List of dicts with keys: 'class_id', 'x_c', 'y_c', 'w', 'h'
    """
    txt_path = Path(txt_path)
    if not txt_path.exists():
        return []
    
    boxes = []
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                boxes.append({
                    "class_id": int(parts[0]),
                    "x_c": float(parts[1]),
                    "y_c": float(parts[2]),
                    "w": float(parts[3]),
                    "h": float(parts[4])
                })
    return boxes


def denormalize_boxes(
    boxes: Union[List[Tuple[float, float, float, float]], np.ndarray, torch.Tensor],
    width: int,
    height: int
) -> np.ndarray:
    """
    Convert normalized [x_c, y_c, w, h] to pixel coordinates [x1, y1, x2, y2].
    
    Args:
        boxes: Array-like of shape (N, 4) in [x_c, y_c, w, h] format, normalized [0, 1].
        width: Image width in pixels.
        height: Image height in pixels.
        
    Returns:
        np.ndarray of shape (N, 4) in [x1, y1, x2, y2] pixel coordinates.
    """
    if len(boxes) == 0:
        return np.zeros((0, 4), dtype=np.float32)
        
    if isinstance(boxes, torch.Tensor):
        boxes_np = boxes.detach().cpu().numpy()
    else:
        boxes_np = np.asarray(boxes, dtype=np.float32)
        
    x_c = boxes_np[:, 0] * width
    y_c = boxes_np[:, 1] * height
    w = boxes_np[:, 2] * width
    h = boxes_np[:, 3] * height
    
    x1 = x_c - w / 2.0
    y1 = y_c - h / 2.0
    x2 = x_c + w / 2.0
    y2 = y_c + h / 2.0
    
    return np.stack([x1, y1, x2, y2], axis=1)


def normalize_boxes(
    boxes: Union[List[Tuple[float, float, float, float]], np.ndarray, torch.Tensor],
    width: int,
    height: int
) -> np.ndarray:
    """
    Convert pixel coordinates [x1, y1, x2, y2] to normalized [x_c, y_c, w, h].
    
    Args:
        boxes: Array-like of shape (N, 4) in [x1, y1, x2, y2] pixel coordinates.
        width: Image width in pixels.
        height: Image height in pixels.
        
    Returns:
        np.ndarray of shape (N, 4) in [x_c, y_c, w, h] normalized to [0, 1].
    """
    if len(boxes) == 0:
        return np.zeros((0, 4), dtype=np.float32)
        
    if isinstance(boxes, torch.Tensor):
        boxes_np = boxes.detach().cpu().numpy()
    else:
        boxes_np = np.asarray(boxes, dtype=np.float32)
        
    x1 = boxes_np[:, 0]
    y1 = boxes_np[:, 1]
    x2 = boxes_np[:, 2]
    y2 = boxes_np[:, 3]
    
    w = x2 - x1
    h = y2 - y1
    x_c = x1 + w / 2.0
    y_c = y1 + h / 2.0
    
    return np.stack([x_c / width, y_c / height, w / width, h / height], axis=1)


class RadDetDataset(Dataset):
    """
    PyTorch Dataset for RadDet radar spectrum detection.
    
    Loads grayscale spectrogram PNGs and corresponding YOLO .txt annotations.
    """
    def __init__(
        self,
        root_dir: Union[str, Path],
        split: str = "train",
        transform = None
    ):
        self.root_dir = Path(root_dir)
        self.split = split
        self.transform = transform
        
        self.images_dir = self.root_dir / "images" / split
        self.labels_dir = self.root_dir / "labels" / split
        
        if not self.images_dir.exists():
            raise FileNotFoundError(f"Images directory not found: {self.images_dir}")
            
        # Collect all image files
        self.image_files = sorted(list(self.images_dir.glob("*.png")) + list(self.images_dir.glob("*.jpg")))
        
    def __len__(self) -> int:
        return len(self.image_files)
        
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        img_path = self.image_files[idx]
        txt_path = self.labels_dir / f"{img_path.stem}.txt"
        
        # Load image as grayscale float tensor (1, H, W) in [0, 1]
        with Image.open(img_path) as pil_img:
            pil_img = pil_img.convert("L")
            img_arr = np.array(pil_img, dtype=np.float32) / 255.0
            
        img_tensor = torch.from_numpy(img_arr).unsqueeze(0)  # (1, H, W)
        
        # Parse annotations
        raw_boxes = load_yolo_annotations(txt_path)
        
        if len(raw_boxes) > 0:
            boxes_norm = np.array([[b["x_c"], b["y_c"], b["w"], b["h"]] for b in raw_boxes], dtype=np.float32)
            classes = np.array([b["class_id"] for b in raw_boxes], dtype=np.int64)
            boxes_tensor = torch.from_numpy(boxes_norm)
            classes_tensor = torch.from_numpy(classes)
        else:
            boxes_tensor = torch.zeros((0, 4), dtype=torch.float32)
            classes_tensor = torch.zeros((0,), dtype=torch.int64)
            
        targets = {
            "boxes": boxes_tensor,       # (N, 4) in [x_c, y_c, w, h] normalized
            "labels": classes_tensor,    # (N,) class indices
            "image_id": torch.tensor([idx], dtype=torch.int64)
        }
        
        if self.transform is not None:
            img_tensor = self.transform(img_tensor)
            
        return img_tensor, targets

