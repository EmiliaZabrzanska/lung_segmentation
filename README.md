# HDS-M03 Mini Project — Lung Segmentation from Chest X-rays

Healthcare Data Science CDT, University of Oxford, Michaelmas 2026
Introduction to Medical Image Analysis

## Overview

This repository contains the code for the mini project on segmentation of lungs from chest X-rays
using basic image processing techniques, applied to the Montgomery County X-ray set
(138 X-rays: 80 normal cases and 58 cases with manifestations of tuberculosis, each with
radiologist-supervised masks of the left and right lung).

All code, commentary and results are in a single notebook, `solution.ipynb`, which follows the
numbered steps (1)–(9) of the project instructions.

## Aims

1. Compare thresholding methods for segmenting the lungs: a naive mean threshold, the best "supervised"
   threshold chosen using the ground truth, and Otsu's unsupervised threshold.
2. Measure how much filtering and morphological post-processing improve the thresholded masks.
3. Compare segmentation quality on normal vs TB cases using the radiologist's masks and the Dice coefficient.
4. Test whether GLCM texture features inside the lungs separate normal from TB cases, and build a simple classifier.

## Approach

The project builds up a classical (non-deep-learning) segmentation pipeline one step at a time, where
each step fixes a problem that is visible in the previous one:

- **Part 1 — Preparing the data (steps 1–3):** load and visualise the X-rays and ground truth, and resize
  to 512 × 512. Lungs appear dark on X-ray, which suggests intensity thresholding as a starting point.
- **Part 2 — Thresholding (steps 4–5):** compare the mean threshold, the best threshold chosen using the
  ground truth, and Otsu's method on one image, using the histogram and the Dice score. This shows that
  thresholding alone also selects the air outside the body and leaves holes and specks.
- **Part 3 — Further processing and assessment (steps 6–8):** add Gaussian smoothing, opening, clear border,
  keeping the two largest regions, hole filling and closing, each targeting one of those problems. The
  pipeline is then run on every normal and TB case, comparing four versions (mean / Otsu, with / without
  post-processing) using Dice and Jaccard, and the worst cases are inspected to understand the failures.
- **Part 4 — Classification (step 9):** compute GLCM texture features inside the lung masks, compare the
  two classes with a scatter plot and Mann-Whitney U tests, and classify normal vs TB with logistic
  regression and stratified 5-fold cross-validation.

## Course Material Used

| Technique | Practical notebook(s) used as a starting point |
|---|---|
| Loading and displaying images | `biomedia_intro_00_read_image` |
| Global thresholding and histograms | `biomedia_intro_03_threshold` |
| Otsu's method | `biomedia_seg_01_otsu` |
| Gaussian smoothing | `biomedia_filters_01_gaussian` |
| Erosion, dilation, opening, closing | `biomedia_intro_04_erosion` – `biomedia_intro_07_closing` |
| Connected components and region labelling | `biomedia_seg_00_label_image`, `biomedia_seg_02_connected_comp` |
| Grey-level co-occurrence matrix | `biomedia_features_05_GLCM` |
| Logistic regression classifier | `biomedia_classification_04_logistic_regression` |

All practical notebooks are from
[engs1258/biomedical-image-analysis-notebooks](https://github.com/engs1258/biomedical-image-analysis-notebooks/wiki).

## Repository Structure

```
m03_lung_segmentation/
├── solution.ipynb      # all code, commentary and results (steps 1–9)
├── data/               # Montgomery X-ray set (not version-controlled)
├── figures/            # generated figures for the slides (PDF)
├── results/            # generated result tables (CSV)
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt    # dependencies
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

Download `MontgomerySet.zip` from Canvas and unzip it into `data/` (see [`data/README.md`](data/README.md)).

## Usage

```bash
jupyter notebook solution.ipynb
```

Run all cells from top to bottom (**Kernel → Restart & Run All**). Figures are saved to `figures/` and
result tables to `results/`. The full data set takes a few minutes; set `N_PER_CLASS` in Part 3 to a
small number for a quick test.

## Declaration of Use of Autogeneration Tools

<!-- TODO: write your own accurate declaration here before submitting. -->

## License

See [LICENSE](LICENSE).
