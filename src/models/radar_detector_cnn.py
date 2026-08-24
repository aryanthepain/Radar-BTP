"""
Radar Object Detection and Semantic Classification CNN (PyTorch)
Detects targets on Range-Doppler maps and regresses continuous coordinates (Range, Velocity, Class).
"""
from typing import Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F
from src.models.radar_dataset import NUM_CLASSES

class ResidualBlock(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.relu = nn.LeakyReLU(0.1, inplace=True)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        return self.relu(out + residual)

class RadarObjectDetectorCNN(nn.Module):
    """
    Fully Convolutional Radar Object Detector for Range-Doppler heatmaps.
    Outputs:
      1. Class Heatmaps (num_classes, H, W)
      2. Coordinate Regressions (4, H, W) -> [range_center, velocity_center, range_width, velocity_width]
    """

    def __init__(self, in_channels: int = 1, num_classes: int = NUM_CLASSES, base_filters: int = 32):
        super().__init__()
        
        # Stem / Input layer
        self.stem = nn.Sequential(
            nn.Conv2d(in_channels, base_filters, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(base_filters),
            nn.LeakyReLU(0.1, inplace=True)
        )

        # Feature extraction backbone
        self.res1 = ResidualBlock(base_filters)
        self.res2 = ResidualBlock(base_filters)

        self.expand = nn.Sequential(
            nn.Conv2d(base_filters, base_filters * 2, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(base_filters * 2),
            nn.LeakyReLU(0.1, inplace=True)
        )

        self.res3 = ResidualBlock(base_filters * 2)
        self.res4 = ResidualBlock(base_filters * 2)

        # Classification / Detection Head
        self.cls_head = nn.Sequential(
            nn.Conv2d(base_filters * 2, base_filters, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(base_filters),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(base_filters, num_classes, kernel_size=1)
        )

        # Box Coordinate Regression Head
        self.box_head = nn.Sequential(
            nn.Conv2d(base_filters * 2, base_filters, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(base_filters),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(base_filters, 4, kernel_size=1),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor):
        feat = self.stem(x)
        feat = self.res1(feat)
        feat = self.res2(feat)
        feat = self.expand(feat)
        feat = self.res3(feat)
        feat = self.res4(feat)

        cls_logits = self.cls_head(feat)
        box_preds = self.box_head(feat)
        return cls_logits, box_preds

    @staticmethod
    def compute_loss(
        cls_logits: torch.Tensor,
        box_preds: torch.Tensor,
        heatmap_targets: torch.Tensor,
        box_targets: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Computes composite multi-task loss:
        - BCE / Focal loss for heatmap class detection
        - Masked Smooth L1 Loss for bounding box regression
        """
        # Heatmap classification loss (BCEWithLogitsLoss)
        cls_loss = F.binary_cross_entropy_with_logits(cls_logits, heatmap_targets)

        # Foreground mask (any non-background class > 0.3)
        fg_mask = (torch.max(heatmap_targets[:, 1:], dim=1, keepdim=True)[0] > 0.3).expand_as(box_preds)

        if fg_mask.sum() > 0:
            box_loss = F.smooth_l1_loss(box_preds[fg_mask], box_targets[fg_mask])
        else:
            box_loss = torch.tensor(0.0, device=cls_logits.device)

        total_loss = cls_loss + 2.0 * box_loss
        return total_loss, cls_loss, box_loss
