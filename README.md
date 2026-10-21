# HDS-M03 Mini Project — Lung Segmentation from Chest X-rays

Healthcare Data Science CDT, University of Oxford, Michaelmas 2026
Introduction to Medical Image Analysis

## Overview

This repository contains the code for the mini project on segmentation of lungs from chest X-rays
using basic image processing techniques, applied to the Montgomery County X-ray set
(80 normal cases, 58 cases with manifestations of tuberculosis).

The project covers four parts, following the numbered steps in the project instructions:
- **Part 1:** Preparing the imaging data (steps 1–3)
- **Part 2:** Supervised and unsupervised (Otsu) thresholding (steps 4–5)
- **Part 3:** Filtering, morphological operations and assessment against the ground truth (steps 6–8)
- **Part 4:** GLCM texture features and a normal vs TB classifier (step 9)

All repeated code is placed in `lungseg.py`, so that the notebooks only contain the analysis and commentary.

## Repository Structure

```
m03_lung_segmentation/
├── lungseg.py                                # helper functions (loading, segmentation, Dice, GLCM)
├── 01_data_exploration.ipynb                 # Part 1
├── 02_thresholding.ipynb                     # Part 2
├── 03_postprocessing_and_evaluation.ipynb    # Part 3
├── 04_glcm_classification.ipynb              # Part 4
├── data/                                     # Montgomery X-ray set (not version-controlled)
├── figures/                                  # generated figures (PDF)
├── results/                                  # generated result tables (CSV)
├── .gitignore
├── LICENSE
├── README.md
├── SETUP.md                                  # step-by-step setup guide
└── requirements.txt                          # dependencies
```

## Installation

Clone the repository, create a virtual environment, and install the dependencies:

```bash
git clone https://github.com/EmiliaZabrzanska/m03_lung_segmentation.git
cd m03_lung_segmentation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The data set should be placed in `data/` as described in [`data/README.md`](data/README.md).
On the CDT server, change `DATA_DIR` at the top of `lungseg.py` to point at the shared copy instead.

## Usage

```bash
jupyter notebook
```

Run the notebooks in order (`01` → `04`). Figures are saved to `figures/` and result tables to `results/`.

## Declaration of Use of Autogeneration Tools

<!-- TODO: write your own accurate declaration here before submitting. -->

## License

See [LICENSE](LICENSE).
