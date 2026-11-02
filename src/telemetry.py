"""Standard In-Container Telemetry Module for Kaggle & Container Workloads.

Implements mandatory automated stage-wise progress logging and Expected Time
to Completion (ETC / ETA) calculation according to global Kaggle workflow rules.
"""

import time
from typing import Optional


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string (e.g. '02m 15s' or '01h 05m 20s')."""
    seconds = max(0, int(seconds))
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}h {m:02d}m {s:02d}s"
    return f"{m:02d}m {s:02d}s"


class StageProgressTracker:
    """In-container telemetry tracker for multi-stage pipelines with automatic ETC/ETA calculation."""

    def __init__(
        self,
        stage_name: str,
        total_items: Optional[int] = None,
        stage_idx: int = 1,
        total_stages: int = 1,
    ):
        self.stage_name = stage_name
        self.total_items = total_items
        self.stage_idx = stage_idx
        self.total_stages = total_stages
        self.start_time = time.time()
        self.processed = 0

    def update(self, step_items: int = 1, extra_info: str = "") -> None:
        self.processed += step_items
        elapsed = time.time() - self.start_time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        stage_prefix = (
            f"[{timestamp}] [INFO] [STAGE {self.stage_idx}/{self.total_stages}: {self.stage_name.upper()}]"
        )

        if self.total_items and self.total_items > 0:
            fraction = min(1.0, self.processed / self.total_items)
            throughput = self.processed / max(elapsed, 0.001)
            remaining_sec = elapsed * (1.0 - fraction) / max(fraction, 0.0001)
            eta_ts = time.strftime("%H:%M:%S", time.localtime(time.time() + remaining_sec))

            print(
                f"{stage_prefix} {self.processed:,}/{self.total_items:,} ({fraction*100:5.1f}%) | "
                f"Elapsed: {format_duration(elapsed)} | Stage ETC: ~{format_duration(remaining_sec)} | "
                f"ETA: {eta_ts} ({throughput:,.1f} items/s)"
                + (f" | {extra_info}" if extra_info else "")
            )
        else:
            print(
                f"{stage_prefix} Processed {self.processed:,} items | Elapsed: {format_duration(elapsed)}"
                + (f" | {extra_info}" if extra_info else "")
            )

    def finish(self) -> None:
        total_time = time.time() - self.start_time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{timestamp}] [SUCCESS] [STAGE {self.stage_idx}/{self.total_stages}: {self.stage_name.upper()}] "
            f"Completed in {format_duration(total_time)}."
        )

