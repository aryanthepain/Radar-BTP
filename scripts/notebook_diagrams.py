"""
Mermaid Diagrams & Collapsible SVG Dual-Embedding Helper for Academic Notebooks
Provides structured Mermaid diagrams for both Classical Radar DSP and Deep Learning Perception,
paired with pre-compiled base64 SVG fallbacks rendered inside collapsible <details> blocks.
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
    # Notebook 1: Classical Radar DSP
    "nb1_top": """graph TD
    A["FMCW Sawtooth Tx Chirps<br/><code>fc = 77 GHz, B = 1 GHz, Tc = 50 us</code>"] --> B["Target Propagation & Reflection<br/><code>Range R, Velocity v, Azimuth theta</code>"]
    B --> C["Homodyne Mixer & Dechirp<br/><code>Beat frequency fb = 2SR/c</code>"]
    C --> D["Raw 3D Radar Cube<br/><code>[4, 128, 256] (Rx x Chirps x Samples) complex64</code>"]
    D --> E["Fast-Time 1D Range FFT<br/><code>RangeProcessor.process()</code><br/><i>Hann windowing</i>"]
    E --> F["Range Profile Cube<br/><code>[4, 128, 256] complex64</code>"]
    F --> G["MTI Clutter Filtering<br/><code>ClutterFilter.filter()</code><br/><i>Slow-time mean subtraction</i>"]
    G --> H["Clutter-Attenuated Cube<br/><code>[4, 128, 256] complex64</code>"]
    H --> I["Slow-Time 2D Doppler FFT<br/><code>DopplerProcessor.process()</code><br/><i>Phase progression delta_phi = 4*pi*v*Tc/lambda</i>"]
    I --> J["Range-Doppler Matrix (RDM)<br/><code>[4, 128, 256] complex64</code>"]
    J --> K["2D CA-CFAR Detection<br/><code>CFARDetector2D.detect()</code><br/><i>Adaptive thresholding T = alpha * P_noise</i>"]
    K --> L["Target Detection Peaks<br/><code>Extracted (R, v)</code>"]
    L --> M["Spatial Array MUSIC AoA<br/><code>AngleEstimator.estimate_aoa_music()</code><br/><i>Subspace eigen-decomposition</i>"]
    M --> N["Direction-of-Arrival theta<br/><code>Super-resolution azimuth angle</code>"]
    N --> O["DBSCAN BEV Clustering<br/><code>RadarClusterer.cluster()</code><br/><i>Polar to Cartesian (x, y)</i>"]
    O --> P["Clustered Cartesian Targets<br/><code>Physical object tracking in BEV</code>"]
    J --> Q["Pedestrian Micro-Doppler STFT<br/><code>DopplerProcessor.compute_micro_doppler_spectrogram()</code>"]
    Q --> R["Time-Frequency Spectrogram<br/><code>Limb articulation & gait cadence</code>"]
""",
    "nb1_sec1": """graph LR
    A["Tx Chirp Generator<br/><code>s_tx(t) = A_tx cos(2*pi*fc*t + pi*S*t^2)</code>"] -->|Carrier: 77 GHz| B["Target Reflection<br/><code>Delay tau = 2(R0 + vt)/c</code>"]
    B -->|Delayed Rx Chirp| C["Homodyne Mixer<br/><code>Dechirp Multiplication</code>"]
    C -->|Low-Pass Filter| D["IF Beat Signal<br/><code>fb = 2SR/c, R = c*fb / (2S)</code>"]
""",
    "nb1_sec2": """graph LR
    A["Traffic Targets<br/><code>Car, Pedestrian, Cyclist (R, v, theta, RCS)</code>"] --> D["FMCW Simulator<br/><code>FMCWRadarSimulator.generate_radar_cube()</code>"]
    B["Ground Clutter<br/><code>Stationary road echoes (Rayleigh)</code>"] --> D
    C["Thermal Noise<br/><code>AWGN (SNR = 18 dB)</code>"] --> D
    D --> E["Raw 3D Radar Cube<br/><code>[4, 128, 256] complex64<br/>(4 Rx x 128 Chirps x 256 Samples)</code>"]
""",
    "nb1_sec3": """graph LR
    A["Raw ADC Cube<br/><code>[4, 128, 256] complex64</code>"] --> B["Fast-Time 1D FFT<br/><code>RangeProcessor.process()</code><br/><i>X[k] = sum w[n]x[n]exp(-j2*pi*k*n/N)</i><br/>Hann Windowing (-31.5 dB sidelobes)"]
    B --> C["Range Profile Cube<br/><code>[4, 128, 256] complex64</code>"]
""",
    "nb1_sec4": """graph LR
    A["Range Profile Cube<br/><code>[4, 128, 256] complex64</code>"] --> B["MTI Clutter Filter<br/><code>ClutterFilter.filter(slow_time_axis=1)</code><br/><i>y[m, n] = x[m, n] - (1/M) sum x[k, n]</i>"]
    B --> C["Clutter-Attenuated Cube<br/><code>[4, 128, 256] complex64<br/>(CA > 18 dB Attenuation)</code>"]
""",
    "nb1_sec5": """graph LR
    A["Clutter-Filtered Cube<br/><code>[4, 128, 256] complex64</code>"] --> B["Slow-Time 2D Doppler FFT<br/><code>DopplerProcessor.process()</code><br/><i>delta_phi = 4*pi*v*Tc/lambda -> v = lambda*fD/2</i><br/>Hann Windowing across chirps"]
    B --> C["Range-Doppler Matrix (RDM)<br/><code>[4, 128, 256] complex64<br/>Calibrated grid in (R, v)</code>"]
""",
    "nb1_sec6": """graph LR
    A["2D Power RDM<br/><code>[128, 256] float64</code>"] --> B["2D CA-CFAR Detector<br/><code>CFARDetector2D.detect()</code><br/><i>CUT vs Guard (2x2) & Training (4x4)</i><br/><i>T = alpha * P_noise, P_FA = 10^-4</i>"]
    B --> C["Detection Peak List<br/><code>Extracted hits: (Range, Velocity, SNR)</code>"]
""",
    "nb1_sec7": """graph LR
    A["Antenna Snapshots<br/><code>[4] complex64 at target (R, v)</code>"] --> B["Spatial Covariance & MUSIC<br/><code>AngleEstimator.estimate_aoa_music()</code><br/><i>R_xx = U_s Lambda_s U_s^H + U_n Lambda_n U_n^H</i><br/><i>P_MUSIC(theta) = 1 / (a^H U_n U_n^H a)</i>"]
    B --> C["Super-Resolution Azimuth<br/><code>Peak angle theta (deg) with sub-degree accuracy</code>"]
""",
    "nb1_sec8": """graph LR
    A["Polar Detections<br/><code>Target points (R, theta, v)</code>"] --> B["DBSCAN & Coordinate Transform<br/><code>RadarClusterer.cluster()</code><br/><i>x = R sin(theta), y = R cos(theta)</i><br/><i>Density clustering & velocity tracking</i>"]
    B --> C["Cartesian BEV Objects<br/><code>Unified physical tracks [x, y, vx, vy]</code>"]
""",
    "nb1_sec9": """graph LR
    A["Slow-Time Returns<br/><code>Pedestrian Range Bin Signal x(t)</code>"] --> B["STFT Micro-Doppler Analysis<br/><code>DopplerProcessor.compute_micro_doppler_spectrogram()</code><br/><i>STFT{x}(t, f) with sliding Hann window</i>"]
    B --> C["Time-Frequency Spectrogram<br/><code>Periodic limb swing harmonics (+/- 150 Hz)</code>"]
""",
    "nb1_sec10": """graph LR
    A["Raw RF Physics<br/>FMCW Chirps"] --> B["Range & Doppler FFT<br/>Spectral Decomposition"]
    B --> C["Statistical CFAR<br/>Hypothesis Testing"]
    C --> D["Array Subspace AoA<br/>Eigen-Analysis"]
    D --> E["Spatial Clustering<br/>DBSCAN BEV"]
    E --> F["Perception Output<br/>Classified Dynamic Tracks"]
""",
    # Notebook 2: Deep Learning Radar Detection
    "nb2_top": """graph TD
    A["FMCW Simulation & Synthesis<br/><code>RadarDataset (Multi-target scenes)</code>"] --> B["RAM Tensor Pre-Caching<br/><code>CachedRadarDataset</code>"]
    B --> C["Normalized RDM Input<br/><code>[B, 1, 128, 129] float32</code>"]
    C --> D["Convolutional Backbone<br/><code>Conv2D 1->32 -> 32->64 + Residual Block</code>"]
    D --> E["Latent Feature Map<br/><code>[B, 64, 128, 129]</code>"]
    E --> F["Classification Head<br/><code>Conv2D 64->32 -> 32->5</code>"]
    E --> G["Bounding Box Head<br/><code>Conv2D 64->32 -> 32->4</code>"]
    F --> H["Class Heatmap Logits<br/><code>[B, 5, 128, 129]</code>"]
    G --> I["Box Regressions<br/><code>[B, 4, 128, 129]</code>"]
    H --> J["Multi-Task Loss<br/><code>L_total = L_cls(BCE) + lambda_box L_box(SmoothL1)</code>"]
    I --> J
    J --> K["AdamW Optimization<br/><code>CosineAnnealingLR Scheduler</code>"]
    K --> L["Trained RadarObjectDetectorCNN"]
    L --> M["Unseen Scene Inference<br/><code>Sigmoid confidence & peak extraction</code>"]
    M --> N["AI Bounding Boxes & Class Labels<br/><code>Car, Pedestrian, Cyclist, Drone</code>"]
""",
    "nb2_sec1": """graph LR
    A["Traffic Targets<br/><code>(Class, Range, Velocity, RCS)</code>"] --> B["Target Bounding Box Encoding<br/><code>Continuous [r, v, w_r, w_v]</code>"]
    A --> C["2D Gaussian Splatting<br/><code>exp(-((d-vk)^2 + (r-rk)^2)/(2*sigma^2))</code>"]
    B --> D["Box Targets Tensor<br/><code>[4, 128, 129] float32</code>"]
    C --> E["Class Heatmaps Tensor<br/><code>[5, 128, 129] float32 (5 classes)</code>"]
    D --> F["Dataset Tuple<br/><code>(RDM, Heatmap, Box)</code>"]
    E --> F
""",
    "nb2_sec2": """graph TD
    A["Input RDM Tensor<br/><code>[B, 1, 128, 129] (Normalized Power)</code>"] --> B["ConvBlock 1<br/><code>Conv2d(1->32, k=3, p=1) + BN + ReLU</code>"]
    B --> C["ConvBlock 2<br/><code>Conv2d(32->64, k=3, p=1) + BN + ReLU</code>"]
    C --> D["Residual Block<br/><code>Conv2d(64->64) + BN + ReLU + Identity</code>"]
    D --> E["Shared Feature Representation<br/><code>[B, 64, 128, 129]</code>"]
    E --> F["Classification Head<br/><code>Conv2d(64->32) -> Conv2d(32->5)</code>"]
    E --> G["Bounding Box Head<br/><code>Conv2d(64->32) -> Conv2d(32->4)</code>"]
    F --> H["Predicted Class Heatmap<br/><code>[B, 5, 128, 129] (Logits)</code>"]
    G --> I["Predicted Box Offsets<br/><code>[B, 4, 128, 129] [r, v, w_r, w_v]</code>"]
    H --> J["Multi-Task Loss Computation<br/><code>BCEWithLogitsLoss(Cls) + SmoothL1(Box on positive bins)</code>"]
    I --> J
    K["Ground Truth Targets<br/><code>Heatmap [B, 5, 128, 129], Box [B, 4, 128, 129]</code>"] --> J
""",
    "nb2_sec3": """graph LR
    A["Cached Dataset<br/><code>32 Radar Scenes</code>"] --> B["Train (80%) / Val (20%) Split<br/><code>Batch size = 6</code>"]
    B --> C["Forward Pass<br/><code>RadarObjectDetectorCNN(RDM)</code>"]
    C --> D["Loss Backpropagation<br/><code>loss.backward() + AdamW step</code>"]
    D --> E["LR Scheduler Step<br/><code>CosineAnnealingLR(T_max=5)</code>"]
    E --> F["Validation Evaluation<br/><code>torch.no_grad() loss tracking</code>"]
""",
    "nb2_sec4": """graph LR
    A["Unseen Test RDM<br/><code>[1, 1, 128, 129]</code>"] --> B["Model Evaluation<br/><code>model.eval(), torch.no_grad()</code>"]
    B --> C["Sigmoid Activation<br/><code>Probabilities sigma(Logits) in [0, 1]</code>"]
    C --> D["Multi-Channel Slicing<br/><code>Car Channel [1], Pedestrian Channel [2]</code>"]
    D --> E["Peak Detection & Spatial Localization<br/><code>Class confidence & kinematics (Range, Velocity)</code>"]
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
    1. Native ```mermaid code block
    2. Collapsible <details> block containing high-resolution SVG fallback (as data:image/svg+xml;base64,...)
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
        finally:
            if os.path.exists(mmd_path):
                os.remove(mmd_path)

    with open(cache_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    b64_svg = base64.b64encode(svg_content.encode("utf-8")).decode("ascii")

    return f"""```mermaid
{mermaid_code.strip()}
```

<details>
<summary><i>Click here to expand fallback diagram if the Mermaid graph above does not render in your environment</i></summary>
<br/>
<p align="center">
  <img src="data:image/svg+xml;base64,{b64_svg}" alt="{fallback_title}" />
</p>
</details>"""
