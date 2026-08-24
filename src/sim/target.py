"""
Radar Target Representation and Multi-target Scenarios
"""
from dataclasses import dataclass
from typing import List, Optional
import numpy as np

@dataclass
class RadarTarget:
    """
    Physical representation of a radar reflecting target.
    
    Attributes:
        range_m: Initial range in meters from radar (R_0).
        velocity_mps: Radial velocity in m/s (+ approaching, - receding or standard convention).
        azimuth_deg: Azimuth angle of arrival in degrees (-90 to +90).
        rcs_dbsm: Radar Cross Section (RCS) in dBsm (e.g. car: +10 dBsm, pedestrian: -5 dBsm, drone: -15 dBsm).
        label: Semantic class label ('car', 'pedestrian', 'cyclist', 'drone', 'clutter').
        micro_doppler_freq: Optional micro-Doppler oscillation frequency in Hz (e.g. gait or propeller).
        micro_doppler_amp: Optional micro-Doppler amplitude in m/s.
    """
    range_m: float
    velocity_mps: float
    azimuth_deg: float
    rcs_dbsm: float = 0.0
    label: str = "target"
    micro_doppler_freq: Optional[float] = None
    micro_doppler_amp: Optional[float] = None

    @property
    def rcs_linear(self) -> float:
        """Linear Radar Cross Section (m^2)."""
        return 10.0 ** (self.rcs_dbsm / 10.0)


def create_standard_traffic_scenario() -> List[RadarTarget]:
    """
    Creates a realistic multi-object autonomous driving scene:
    - Approaching Car (Fast, large RCS, left lane)
    - Receding Vehicle (Moderate speed, center lane)
    - Crossing / Walking Pedestrian (Slow, low RCS, right side, micro-Doppler)
    - Cyclist (Medium speed, right lane)
    """
    return [
        RadarTarget(
            range_m=28.5,
            velocity_mps=-14.2,  # Receding at 14.2 m/s (~51 km/h)
            azimuth_deg=-12.0,
            rcs_dbsm=12.0,
            label="car"
        ),
        RadarTarget(
            range_m=12.0,
            velocity_mps=8.5,    # Approaching at 8.5 m/s (~30 km/h)
            azimuth_deg=18.0,
            rcs_dbsm=8.0,
            label="car"
        ),
        RadarTarget(
            range_m=8.4,
            velocity_mps=1.4,    # Walking pedestrian at 1.4 m/s (5 km/h)
            azimuth_deg=28.0,
            rcs_dbsm=-4.0,
            label="pedestrian",
            micro_doppler_freq=2.0,
            micro_doppler_amp=0.6
        ),
        RadarTarget(
            range_m=19.2,
            velocity_mps=-4.8,   # Cyclist at 4.8 m/s (~17 km/h)
            azimuth_deg=5.0,
            rcs_dbsm=1.0,
            label="cyclist"
        )
    ]
