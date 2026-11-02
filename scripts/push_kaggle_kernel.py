#!/usr/bin/env python3
"""Automated Kaggle Kernel Builder & CLI Push Utility.

Generates kernel-metadata.json, performs deterministic pre-push validation on
notebook structure, and pushes the notebook to Kaggle kernels via the Kaggle CLI.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def get_default_username() -> str:
    """Retrieve Kaggle username from ~/.kaggle/kaggle.json or default to aryanguptaji."""
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    try:
        if kaggle_json.is_file():
            with open(kaggle_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("username", "aryanguptaji")
    except (OSError, PermissionError, Exception):
        pass
    return os.environ.get("KAGGLE_USERNAME", "aryanguptaji")


def validate_notebook(notebook_path: Path) -> dict:
    """Validate that notebook file exists and is valid JSON."""
    if not notebook_path.is_file():
        raise FileNotFoundError(f"Notebook file not found: {notebook_path}")
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb_data = json.load(f)
    except Exception as e:
        raise ValueError(f"Notebook is not valid JSON: {e}") from e

    cells = nb_data.get("cells", [])
    if not cells:
        raise ValueError("Notebook contains zero cells.")
    print(f"  [+] Validated notebook '{notebook_path.name}' ({len(cells)} cells)")
    return nb_data


def build_and_push_kernel(
    notebook_path: Path,
    title: str,
    slug: str,
    username: str,
    datasets: list[str],
    enable_gpu: bool = True,
    enable_internet: bool = True,
    is_private: bool = True,
    push: bool = False,
    build_dir: Path = Path(".kaggle_build"),
) -> Path:
    """Stage metadata and notebook into build directory and optionally push via Kaggle CLI."""
    validate_notebook(notebook_path)

    kernel_id = f"{username}/{slug}"
    target_dir = build_dir / slug
    target_dir.mkdir(parents=True, exist_ok=True)

    target_nb = target_dir / notebook_path.name
    shutil.copy2(notebook_path, target_nb)

    metadata = {
        "id": kernel_id,
        "title": title,
        "code_file": notebook_path.name,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": "true" if is_private else "false",
        "enable_gpu": "true" if enable_gpu else "false",
        "enable_tpu": "false",
        "enable_internet": "true" if enable_internet else "false",
        "dataset_sources": datasets,
        "competition_sources": [],
        "kernel_sources": [],
        "model_sources": [],
    }

    metadata_path = target_dir / "kernel-metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"  [+] Generated kernel metadata: {metadata_path}")
    print(f"      Kernel ID: {kernel_id}")
    print(f"      Datasets: {datasets}")
    print(f"      GPU: {enable_gpu} | Internet: {enable_internet} | Private: {is_private}")

    if push:
        print(f"\n[PUSH] Pushing kernel to Kaggle via 'kaggle kernels push -p {target_dir}'...")
        try:
            res = subprocess.run(
                ["kaggle", "kernels", "push", "-p", str(target_dir)],
                capture_output=True,
                text=True,
                check=True,
            )
            print("  [+] Kaggle CLI Output:")
            print(res.stdout)
            print(f"  [*] Kernel URL: https://www.kaggle.com/code/{kernel_id}")
        except subprocess.CalledProcessError as e:
            print(f"  [!] Error pushing kernel: {e.stderr}", file=sys.stderr)
            raise
    else:
        print(f"\n  [*] Staged in '{target_dir}'. Pass '--push' to deploy to Kaggle.")

    return target_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Kaggle Kernel Staging & Push CLI")
    parser.add_argument(
        "--notebook",
        type=Path,
        default=Path("03_raddet_spectrum_detection_kaggle.ipynb"),
        help="Path to source notebook",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="RadDet Radar Spectrum Detection & Sensing Benchmark",
        help="Kernel title on Kaggle",
    )
    parser.add_argument(
        "--slug",
        type=str,
        default="raddet-spectrum-detection",
        help="Kernel URL slug",
    )
    parser.add_argument(
        "--username",
        type=str,
        default=get_default_username(),
        help="Kaggle username",
    )
    parser.add_argument(
        "--dataset",
        action="append",
        dest="datasets",
        default=[],
        help="Kaggle dataset to attach (can specify multiple)",
    )
    parser.add_argument(
        "--no-gpu",
        dest="enable_gpu",
        action="store_false",
        default=True,
        help="Disable GPU acceleration",
    )
    parser.add_argument(
        "--no-internet",
        dest="enable_internet",
        action="store_false",
        default=True,
        help="Disable internet access in kernel",
    )
    parser.add_argument(
        "--public",
        dest="is_private",
        action="store_false",
        default=True,
        help="Make kernel publicly visible",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Execute 'kaggle kernels push' after staging",
    )

    args = parser.parse_args()

    datasets = args.datasets or ["abcxyzi/raddet-icassp-2025"]

    build_and_push_kernel(
        notebook_path=args.notebook,
        title=args.title,
        slug=args.slug,
        username=args.username,
        datasets=datasets,
        enable_gpu=args.enable_gpu,
        enable_internet=args.enable_internet,
        is_private=args.is_private,
        push=args.push,
    )


if __name__ == "__main__":
    main()
