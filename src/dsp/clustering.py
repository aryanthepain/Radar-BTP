"""
Radar Point Cloud Clustering and Object Entity Extraction Module
Transforms CFAR detections into Cartesian BEV space and clusters reflections via DBSCAN.
"""
import os
os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(os.cpu_count() or 4))
from typing import List, Dict
import numpy as np
from sklearn.cluster import DBSCAN

class RadarClusterer:
    """
    Groups radar point detections into discrete objects using DBSCAN in Cartesian/Doppler space.
    """

    def __init__(self, eps: float = 1.5, min_samples: int = 1):
        self.eps = eps
        self.min_samples = min_samples
        self.dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples, n_jobs=1)

    def cluster_detections(self, detections: List[Dict[str, float]]) -> List[Dict[str, float]]:
        """
        Takes CFAR detections with 'range_m', 'velocity_mps', 'azimuth_deg' and groups into objects.
        
        Returns:
            clustered_objects: List of object dictionaries with centroid (x, y, range, velocity, angle) and bounds.
        """
        if not detections:
            return []

        # Convert to Cartesian BEV: X = R * sin(theta), Y = R * cos(theta)
        ranges = np.array([d["range_m"] for d in detections])
        velocities = np.array([d["velocity_mps"] for d in detections])
        angles_deg = np.array([d.get("azimuth_deg", 0.0) for d in detections])
        angles_rad = np.deg2rad(angles_deg)

        xs = ranges * np.sin(angles_rad)
        ys = ranges * np.cos(angles_rad)

        # Feature matrix for clustering: [X, Y, normalized_velocity]
        features = np.column_stack([xs, ys, velocities * 0.2])
        labels = self.dbscan.fit_predict(features)

        unique_labels = set(labels)
        objects = []

        for lab in unique_labels:
            if lab == -1:
                # Noise points
                continue

            mask = (labels == lab)
            cluster_xs = xs[mask]
            cluster_ys = ys[mask]
            cluster_vels = velocities[mask]
            cluster_ranges = ranges[mask]
            cluster_angles = angles_deg[mask]
            cluster_powers = [detections[i]["peak_power"] for i in range(len(detections)) if mask[i]]

            # Weighted or mean centroid
            x_cent = float(np.mean(cluster_xs))
            y_cent = float(np.mean(cluster_ys))
            r_cent = float(np.sqrt(x_cent**2 + y_cent**2))
            v_cent = float(np.mean(cluster_vels))
            th_cent = float(np.rad2deg(np.arctan2(x_cent, y_cent)))
            total_power = float(np.sum(cluster_powers))

            objects.append({
                "object_id": int(lab),
                "num_points": int(np.sum(mask)),
                "x_m": x_cent,
                "y_m": y_cent,
                "range_m": r_cent,
                "velocity_mps": v_cent,
                "azimuth_deg": th_cent,
                "total_power": total_power,
                "bbox_x_min": float(np.min(cluster_xs)),
                "bbox_x_max": float(np.max(cluster_xs)),
                "bbox_y_min": float(np.min(cluster_ys)),
                "bbox_y_max": float(np.max(cluster_ys))
            })

        return objects
