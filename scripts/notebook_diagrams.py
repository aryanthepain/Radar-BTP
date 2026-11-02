"""
Mermaid Diagrams & Collapsible SVG Dual-Embedding Helper for Academic Notebooks
Provides structured Mermaid diagrams for both Classical Radar DSP and Deep Learning Perception,
paired with pre-compiled base64 SVG fallbacks rendered as the primary visual,
and Mermaid source code encapsulated inside collapsible <details> blocks.
"""
import os
import sys
import base64
import hashlib
import subprocess
import tempfile

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CACHE_DIR = os.path.join(ROOT_DIR, ".cache", "mermaid")

DIAGRAMS = {
    # Notebook 1: Classical Radar DSP — Snake Flow (4 Rows)
    "nb1_top": """flowchart TD
    subgraph Row1 ["Stage 1: RF Chirp Synthesis & Raw ADC Cube Acquisition"]
        direction LR
        A["FMCW Sawtooth Tx Chirps"] --> B["Target Propagation & Echo Delay"] --> C["Homodyne Mixer & Dechirp"] --> D["Raw 3D Radar Cube"]
    end

    subgraph Row2 ["Stage 2: Range & Doppler Spectral Decomposition"]
        direction RL
        E["Fast-Time 1D Range FFT"] --> F["Range Profile Cube"] --> G["MTI Clutter Subtraction"] --> H["Slow-Time 2D Doppler FFT"] --> I["Range-Doppler Matrix (RDM)"]
    end

    subgraph Row3 ["Stage 3: Statistical Detection & Spatial AoA Tracking"]
        direction LR
        J["2D CA-CFAR Detection"] --> K["Extracted Target Peaks"] --> L["Spatial Array MUSIC AoA"] --> M["DBSCAN BEV Clustering"] --> N["Classified Cartesian Tracks"]
    end

    subgraph Row4 ["Stage 4: Micro-Doppler Time-Frequency Articulation"]
        direction LR
        O["Pedestrian Slow-Time Returns"] --> P["STFT Spectrogram Analysis"] --> Q["Pedestrian Gait Cadence"]
    end

    D --> E
    I --> J
    I --> O
""",
    "nb1_sec1": """graph LR
    A["Tx Chirp Generator"] -->|RF Carrier| B["Target Propagation & Echo"]
    B -->|Delayed Rx Chirp| C["Homodyne Mixer"]
    C -->|Low-Pass Filter| D["IF Beat Frequency Signal"]
""",
    "nb1_sec2": """graph LR
    A["Traffic Targets"] --> D["FMCW Radar Simulator"]
    B["Ground Clutter"] --> D
    C["Thermal Noise"] --> D
    D --> E["Raw 3D Radar Cube"]
""",
    "nb1_sec3": """graph LR
    A["Raw ADC Cube"] --> B["Fast-Time 1D FFT & Hann Windowing"]
    B --> C["Range Profile Cube"]
""",
    "nb1_sec4": """graph LR
    A["Range Profile Cube"] --> B["MTI Clutter Subtraction Filter"]
    B --> C["Clutter-Attenuated Cube"]
""",
    "nb1_sec5": """graph LR
    A["Clutter-Filtered Cube"] --> B["Slow-Time 2D Doppler FFT"]
    B --> C["Range-Doppler Matrix"]
""",
    "nb1_sec6": """graph LR
    A["2D Power RDM"] --> B["2D CA-CFAR Adaptive Detector"]
    B --> C["Target Detection Peak List"]
""",
    "nb1_sec7": """graph LR
    A["Antenna Snapshots across ULA"] --> B["Spatial Covariance & MUSIC Subspace Decomposition"]
    B --> C["Super-Resolution Azimuth AoA"]
""",
    "nb1_sec8": """graph LR
    A["Polar Detections"] --> B["Coordinate Transform & DBSCAN Clustering"]
    B --> C["Cartesian BEV Object Tracks"]
""",
    "nb1_sec9": """graph LR
    A["Pedestrian Slow-Time Returns"] --> B["STFT Time-Frequency Analysis"]
    B --> C["Micro-Doppler Spectrogram"]
""",
    "nb1_sec10": """graph LR
    A["Raw RF Physics<br/>FMCW Chirps"] --> B["Range & Doppler FFT<br/>Spectral Decomposition"]
    B --> C["Statistical CFAR<br/>Hypothesis Testing"]
    C --> D["Array Subspace AoA<br/>Eigen-Analysis"]
    D --> E["Spatial Clustering<br/>DBSCAN BEV"]
    E --> F["Perception Output<br/>Classified Dynamic Tracks"]
""",

    # Notebook 3: RadDet Spectrum Detection & Sensing Benchmark
    "nb3_top": """flowchart TD
    subgraph Row1 ["Stage 1: RF Front-End & Wideband Baseband I/Q Acquisition"]
        direction LR
        A["500 MHz Wideband RF Environment"] --> B["1M Complex I/Q Samples (2 ms)"] --> C["STFT Time-Frequency Analysis"] --> D["Max-Hold Spectrogram Compression"]
    end

    subgraph Row2 ["Stage 2: Spectrogram Normalization & YOLO Bounding Boxes"]
        direction RL
        E["128x128 Max-Hold Spectrogram"] --> F["YOLO Ground-Truth Annotations"] --> G["11 Radar Modulation Classes"] --> H["Batch Tensor Preparation"]
    end

    subgraph Row3 ["Stage 3: Deep Feature Pyramid & Detection Backbone"]
        direction LR
        I["YOLOv8 Darknet Backbone"] --> J["C2f Feature Extraction"] --> K["PANet Feature Pyramid"] --> L["Decoupled Detection Heads"]
    end

    subgraph Row4 ["Stage 4: Cognitive EW Inference & mAP Evaluation"]
        direction RL
        M["Real-Time Spectrogram Inference"] --> N["NMS Bounding Box Regression"] --> O["Quantitative mAP50 / mAP50:95"] --> P["High-Contrast Detection Overlays"]
    end

    D --> E
    H --> I
    L --> M
""",
    "nb3_sec1": """graph LR
    A["Wideband RF Signals"] --> B["1M Baseband I/Q Samples"]
    B --> C["Short-Time Fourier Transform"]
    C --> D["Max-Hold Pooling Across Time/Freq"]
    D --> E["128x128 Spectrogram Representation"]
""",
    "nb2_top": """flowchart TD
    subgraph Row1 ["Stage 1: Multi-Target Simulation & Tensor Preparation"]
        direction LR
        A["FMCW Radar Simulation"] --> B["Multi-Target Radar Scenes"] --> C["RAM Tensor Pre-Caching"] --> D["Normalized RDM Input"]
    end

    subgraph Row2 ["Stage 2: Deep Feature Extraction Backbone"]
        direction RL
        E["Initial ConvBlock"] --> F["Deep ConvBlock"] --> G["Residual Skip Block"] --> H["Latent Feature Map"]
    end

    subgraph Row3 ["Stage 3: Multi-Task Perception Heads & Loss Formulation"]
        direction LR
        I["Classification Head"] --> K["Multi-Task Loss Optimization"]
        J["Bounding Box Head"] --> K
        H --> I
        H --> J
    end

    subgraph Row4 ["Stage 4: Inference & Semantic Object Detection"]
        direction RL
        L["Trained Radar CNN"] --> M["Unseen Scene RDM"] --> N["Sigmoid Peak Extraction"] --> O["Bounding Boxes & Class Labels"]
    end

    D --> E
    K --> L
""",
    "nb2_sec1": """graph LR
    A["Multi-Target Scenario"] --> B["Bounding Box Parameterization"]
    A --> C["2D Gaussian Heatmap Splatting"]
    B --> D["Bounding Box Target Tensor"]
    C --> E["Semantic Class Heatmaps"]
    D --> F["Training Dataset Sample"]
    E --> F
""",
    "nb2_sec2": """graph TD
    A["Input RDM Tensor"] --> B["Convolutional Stage 1"]
    B --> C["Convolutional Stage 2"]
    C --> D["Residual Bottleneck Block"]
    D --> E["Shared Feature Representation"]
    E --> F["Classification Head"]
    E --> G["Bounding Box Head"]
    F --> H["Predicted Class Heatmaps"]
    G --> I["Predicted Box Coordinates"]
    H --> J["Multi-Task Loss Function"]
    I --> J
    K["Ground Truth Heatmap & Box Targets"] --> J
""",
    "nb2_sec3": """graph LR
    A["Cached Radar Dataset"] --> B["Train & Validation Split"]
    B --> C["Forward Pass"]
    C --> D["Loss Backpropagation & Optimizer Step"]
    D --> E["Learning Rate Scheduler Update"]
    E --> F["Validation Evaluation"]
""",
    "nb2_sec4": """graph LR
    A["Unseen Test RDM"] --> B["Model Inference"]
    B --> C["Sigmoid Confidence Calibration"]
    C --> D["Multi-Channel Class Slicing"]
    D --> E["Peak Detection & Object Localization"]
""",
    "nb2_sec5": """graph TD
    subgraph Classical_Pipeline ["Classical Radar DSP Pipeline"]
        C1["Raw ADC Radar Cube"] --> C2["1D Range FFT"]
        C2 --> C3["MTI Clutter Subtraction"]
        C3 --> C4["2D Doppler FFT"]
        C4 --> C5["2D CA-CFAR Thresholding"]
        C5 --> C6["MUSIC Subspace AoA"]
        C6 --> C7["DBSCAN Clustering & BEV"]
    end

    subgraph Deep_Learning_Pipeline ["Deep Learning Radar Pipeline"]
        D1["Range-Doppler Power Map"] --> D2["Fully Convolutional Backbone"]
        D2 --> D3["Latent Feature Map"]
        D3 --> D4["Classification Head (Heatmap)"]
        D3 --> D5["Bounding Box Head (Regression)"]
        D4 --> D6["Simultaneous Class & Box Bounding"]
        D5 --> D6
    end

    C7 -.-> M["Pedagogical Integration & Comparison"]
    D6 -.-> M
"""
}

def render_mermaid_dual_block(mermaid_code: str, fallback_title: str = "Fallback Architecture Diagram") -> str:
    """
    Renders a dual-embedding block:
    1. Primary high-resolution embedded SVG (rendered directly in markdown).
    2. Collapsible <details> block containing the raw Mermaid source code.
    SVGs are compiled via `npx -y @mermaid-js/mermaid-cli` and cached on disk in .cache/mermaid/.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    code_hash = hashlib.sha256(mermaid_code.strip().encode("utf-8")).hexdigest()[:16]
    cache_path = os.path.join(CACHE_DIR, f"{code_hash}.svg")

    if not os.path.exists(cache_path):
        with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False, encoding="utf-8") as tf:
            tf.write(mermaid_code.strip())
            mmd_path = tf.name
        try:
            npx_cmd = "npx.cmd" if sys.platform == "win32" else "npx"
            subprocess.run(
                [npx_cmd, "-y", "@mermaid-js/mermaid-cli", "-i", mmd_path, "-o", cache_path, "-b", "transparent"],
                check=True,
                capture_output=True
            )
        except Exception:
            pass
        finally:
            if os.path.exists(mmd_path):
                os.remove(mmd_path)

    if not os.path.exists(cache_path):
        return f"""<details open>
<summary><b>{fallback_title} (Mermaid Pipeline Flow)</b></summary>

```mermaid
{mermaid_code.strip()}
```

</details>"""

    with open(cache_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    b64_svg = base64.b64encode(svg_content.encode("utf-8")).decode("ascii")

    return f"""<p align="center">
  <img src="data:image/svg+xml;base64,{b64_svg}" alt="{fallback_title}" style="max-width: 100%; height: auto;" />
</p>

<details>
<summary><i>Click to inspect Mermaid diagram source code</i></summary>

```mermaid
{mermaid_code.strip()}
```

</details>"""
