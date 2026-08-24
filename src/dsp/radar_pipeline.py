"""
Unified Classical Radar DSP Pipeline
Chains Range FFT -> MTI Clutter Filter -> Doppler FFT -> 2D CFAR -> AoA MUSIC -> DBSCAN Clustering.
"""
from typing import List, Dict, Tuple, Optional
import numpy as np
from src.sim.radar_config import RadarConfig
from src.sim.target import RadarTarget
from src.sim.radar_sim import FMCWRadarSimulator
from src.dsp.range_processing import RangeProcessor
from src.dsp.clutter_removal import ClutterFilter
from src.dsp.doppler_processing import DopplerProcessor
from src.dsp.cfar_detector import CFARDetector2D
from src.dsp.aoa_estimation import AngleEstimator
from src.dsp.clustering import RadarClusterer

class ClassicalRadarPipeline:
    """
    End-to-end Classical Radar Signal Processing and Object Detection Pipeline.
    """

    def __init__(
        self,
        config: Optional[RadarConfig] = None,
        cfar_type: str = "ca",
        p_fa: float = 1e-4,
        clutter_method: str = "mean_subtraction"
    ):
        self.config = config or RadarConfig()
        self.range_proc = RangeProcessor(self.config, window="hann")
        self.clutter_filter = ClutterFilter(method=clutter_method)
        self.doppler_proc = DopplerProcessor(self.config, window="hann")
        self.cfar_detector = CFARDetector2D(
            num_train_range=4,
            num_train_doppler=4,
            num_guard_range=2,
            num_guard_doppler=2,
            p_fa=p_fa,
            cfar_type=cfar_type
        )
        self.aoa_estimator = AngleEstimator(self.config, num_angle_bins=181)
        self.clusterer = RadarClusterer(eps=2.0, min_samples=1)

    def process_radar_cube(self, radar_cube: np.ndarray) -> Dict:
        """
        Executes complete DSP chain on 3D raw radar cube (num_rx, num_chirps, num_samples).
        
        Returns:
            Dictionary containing:
            - 'range_profile': 1D range profile across chirps
            - 'filtered_range_profile': Range profile after MTI clutter suppression
            - 'rdm': 2D Range-Doppler Matrix
            - 'rdm_power_db': RDM in dB scale
            - 'detection_mask': 2D boolean CFAR mask
            - 'threshold_map': 2D CFAR threshold map
            - 'raw_detections': List of CFAR detected peaks with AoA
            - 'detected_objects': List of clustered object entities
            - 'clutter_attenuation_db': Clutter suppression metric
        """
        # Step 1: 1D Fast-Time Range FFT
        range_cube, range_axis = self.range_proc.process(radar_cube)

        # Step 2: MTI Clutter Filtering
        filtered_range_cube = self.clutter_filter.filter(range_cube, slow_time_axis=1)
        ca_db = ClutterFilter.compute_clutter_attenuation_db(range_cube, filtered_range_cube)

        # Step 3: 2D Slow-Time Doppler FFT
        rdm, velocity_axis, _ = self.doppler_proc.process(filtered_range_cube)
        rdm_power_linear = np.mean(np.abs(rdm)**2, axis=0)
        rdm_power_db = 10.0 * np.log10(np.maximum(rdm_power_linear, 1e-12))

        # Step 4: 2D CFAR Target Detection
        det_mask, thresh_map, detections = self.cfar_detector.detect(
            rdm_power=rdm_power_linear,
            range_axis=range_axis,
            velocity_axis=velocity_axis
        )

        # Step 5: AoA Estimation for each detected peak
        for det in detections:
            r_bin = det["range_bin"]
            d_bin = det["doppler_bin"]
            
            # Extract antenna snapshots at this (doppler, range) bin across all Rx antennas
            # rdm shape: (num_rx, num_doppler, num_range)
            rx_vector = rdm[:, d_bin, r_bin]
            
            # Subspace MUSIC AoA estimation
            _, _, est_angle_music = self.aoa_estimator.estimate_aoa_music(rx_vector, num_sources=1)
            det["azimuth_deg"] = est_angle_music

        # Step 6: DBSCAN Spatial Clustering
        objects = self.clusterer.cluster_detections(detections)

        return {
            "range_cube": range_cube,
            "filtered_range_cube": filtered_range_cube,
            "rdm": rdm,
            "rdm_power_db": rdm_power_db,
            "range_axis": range_axis,
            "velocity_axis": velocity_axis,
            "detection_mask": det_mask,
            "threshold_map": thresh_map,
            "raw_detections": detections,
            "detected_objects": objects,
            "clutter_attenuation_db": ca_db
        }
