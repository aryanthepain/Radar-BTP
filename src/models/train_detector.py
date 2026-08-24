"""
Training and Evaluation Script for Radar Object Detector CNN
"""
import time
from typing import Dict, Tuple, List
import numpy as np
import torch
from torch.utils.data import DataLoader, random_split
from src.models.radar_dataset import RadarDataset, CLASS_MAP, NUM_CLASSES
from src.models.radar_detector_cnn import RadarObjectDetectorCNN

def train_radar_detector(
    num_samples: int = 150,
    epochs: int = 5,
    batch_size: int = 8,
    lr: float = 1e-3,
    device_str: str = "cpu"
) -> Tuple[RadarObjectDetectorCNN, Dict[str, List[float]]]:
    """
    Trains the RadarObjectDetectorCNN on synthetic radar dataset.
    """
    device = torch.device(device_str if torch.cuda.is_available() and device_str == "cuda" else "cpu")
    print(f"[*] Initializing Radar Dataset with {num_samples} frames...")
    full_dataset = RadarDataset(num_samples=num_samples)
    
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_set, val_set = random_split(full_dataset, [train_size, val_size])

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False)

    model = RadarObjectDetectorCNN(in_channels=1, num_classes=NUM_CLASSES).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    history = {"train_loss": [], "val_loss": [], "cls_loss": [], "box_loss": []}

    print(f"[*] Starting Training for {epochs} epochs on device: {device}...")
    start_time = time.time()

    for epoch in range(1, epochs + 1):
        model.train()
        epoch_train_loss = 0.0
        epoch_cls_loss = 0.0
        epoch_box_loss = 0.0

        for rdm, heatmap_target, box_target in train_loader:
            rdm = rdm.to(device)
            heatmap_target = heatmap_target.to(device)
            box_target = box_target.to(device)

            optimizer.zero_grad()
            cls_logits, box_preds = model(rdm)
            total_loss, cls_loss, box_loss = model.compute_loss(
                cls_logits, box_preds, heatmap_target, box_target
            )
            total_loss.backward()
            optimizer.step()

            epoch_train_loss += total_loss.item() * len(rdm)
            epoch_cls_loss += cls_loss.item() * len(rdm)
            epoch_box_loss += box_loss.item() * len(rdm)

        scheduler.step()

        # Validation
        model.eval()
        epoch_val_loss = 0.0
        with torch.no_grad():
            for rdm, heatmap_target, box_target in val_loader:
                rdm = rdm.to(device)
                heatmap_target = heatmap_target.to(device)
                box_target = box_target.to(device)

                cls_logits, box_preds = model(rdm)
                val_loss, _, _ = model.compute_loss(cls_logits, box_preds, heatmap_target, box_target)
                epoch_val_loss += val_loss.item() * len(rdm)

        train_loss_avg = epoch_train_loss / train_size
        val_loss_avg = epoch_val_loss / val_size
        cls_loss_avg = epoch_cls_loss / train_size
        box_loss_avg = epoch_box_loss / train_size

        history["train_loss"].append(train_loss_avg)
        history["val_loss"].append(val_loss_avg)
        history["cls_loss"].append(cls_loss_avg)
        history["box_loss"].append(box_loss_avg)

        print(f"Epoch [{epoch}/{epochs}] | Train Loss: {train_loss_avg:.4f} | Val Loss: {val_loss_avg:.4f} (Cls: {cls_loss_avg:.4f}, Box: {box_loss_avg:.4f})")

    elapsed = time.time() - start_time
    print(f"[+] Training completed in {elapsed:.2f}s.")
    return model, history
