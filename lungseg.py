"""
lungseg
=======

Helper functions for the HDS-M03 mini project: segmentation of lungs from
chest X-rays using basic image processing, followed by GLCM texture
classification of normal vs tuberculosis (TB) cases.

All repetitive code lives here so that the notebooks stay short and every
step is defined in one place.

Functions
---------
get_label
    Read the normal / TB label from a file name (steps 1-3).
list_cases
    List the X-ray file names, optionally for one class only (steps 1-3).
load_case
    Load and resize one X-ray and its ground-truth lung mask (steps 1-3).
keep_largest_regions
    Keep the n largest connected regions of a binary mask (step 6).
segment_lungs
    Full pipeline: smoothing, thresholding and morphological clean-up (steps 4-6).
dice, jaccard
    Overlap scores against the ground truth (steps 7-8).
glcm_features
    GLCM texture features computed inside the lung mask only (step 9).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from skimage import filters, io, measure, morphology, transform, util
from skimage.feature import graycomatrix, graycoprops
from skimage.segmentation import clear_border


# ---------------------------------------------------------------------------
# Paths and constants (the only lines that should need changing)
# ---------------------------------------------------------------------------

# folder containing the unzipped Montgomery set
# on the CDT server use Path('/data/cdtshared/Cohort-2024/HDS-M03/MontgomerySet')
DATA_DIR   = Path('data/MontgomerySet')

# sub-folders matching the official NLM zip, change if your copy differs
IMAGE_DIR  = DATA_DIR / 'CXR_png'
LEFT_DIR   = DATA_DIR / 'ManualMask' / 'leftMask'
RIGHT_DIR  = DATA_DIR / 'ManualMask' / 'rightMask'

# originals are up to 4892 x 4020 pixels, so resize everything for speed
IMAGE_SIZE = (512, 512)

# GLCM properties computed in step 9 (all built into scikit-image)
GLCM_PROPS = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation']


# ---------------------------------------------------------------------------
# Steps 1-3: loading and resampling the data
# ---------------------------------------------------------------------------

def get_label(filename):

    """
    Return the class label encoded in a Montgomery file name.

    File names look like ``MCUCXR_0001_0.png``, where the digit before
    ``.png`` is 0 for a normal X-ray and 1 for TB.

    Parameters
    ----------
    filename : str or pathlib.Path
        X-ray file name.

    Returns
    -------
    int
        0 for normal, 1 for TB.
    """

    # the last character of the name without its extension is the label
    return int(Path(filename).stem[-1])


def list_cases(label=None):

    """
    List the X-ray file names in ``IMAGE_DIR``.

    Parameters
    ----------
    label : int or None, optional
        None returns all cases, 0 only normal cases and 1 only TB cases.

    Returns
    -------
    list of str
        Sorted file names, e.g. ``['MCUCXR_0001_0.png', ...]``.
    """

    names = sorted(p.name for p in IMAGE_DIR.glob('*.png'))

    # keep only the requested class, if one was given
    if label is not None:
        names = [n for n in names if get_label(n) == label]

    return names


def load_case(filename, size=IMAGE_SIZE):

    """
    Load one X-ray and its ground-truth lung mask, both resized to ``size``.

    Parameters
    ----------
    filename : str
        X-ray file name (the masks share the same name).
    size : tuple of int, optional
        Output shape (rows, columns). Default is ``IMAGE_SIZE``.

    Returns
    -------
    image : np.ndarray
        2D float array with values in [0, 1] (0 = black, 1 = white).
    mask : np.ndarray
        2D bool array, True where the radiologist marked lung
        (left and right lungs combined).
    """

    # read as a single grey channel and convert any bit depth to floats in [0, 1]
    image = util.img_as_float(io.imread(IMAGE_DIR / filename, as_gray=True))

    # anti-aliasing blurs slightly before shrinking to avoid jagged artefacts
    image = transform.resize(image, size, anti_aliasing=True)

    # masks are stored as 0 (background) and 255 (lung)
    left  = io.imread(LEFT_DIR / filename, as_gray=True) > 0
    right = io.imread(RIGHT_DIR / filename, as_gray=True) > 0

    # logical OR: a pixel is lung if it is in either mask
    mask = left | right

    # order=0 (nearest neighbour) keeps the mask strictly True/False
    mask = transform.resize(mask, size, order=0, anti_aliasing=False) > 0.5

    return image, mask


# ---------------------------------------------------------------------------
# Steps 4-6: thresholding and morphological clean-up
# ---------------------------------------------------------------------------

def keep_largest_regions(binary, n=2):

    """
    Keep only the ``n`` largest connected regions of a binary mask.

    Parameters
    ----------
    binary : np.ndarray
        2D bool array.
    n : int, optional
        Number of regions to keep. Default is 2 (one per lung).

    Returns
    -------
    np.ndarray
        2D bool array containing only the ``n`` largest regions.
    """

    # give each separate region its own integer label
    labels = measure.label(binary)

    # nothing found, so return an empty mask
    if labels.max() == 0:
        return binary.copy()

    # measure every region and sort from largest to smallest area
    regions = sorted(measure.regionprops(labels), key=lambda r: r.area, reverse=True)
    keep    = [r.label for r in regions[:n]]

    # True only for pixels belonging to the kept regions
    return np.isin(labels, keep)


def segment_lungs(image, method='otsu', sigma=2, post_process=True):

    """
    Segment the lungs from a chest X-ray.

    The pipeline is: Gaussian smoothing, a global threshold (mean or Otsu),
    lung = pixels below the threshold (air appears dark), then optionally a
    morphological clean-up: opening, clear border, keep the two largest
    regions, fill holes and closing.

    Parameters
    ----------
    image : np.ndarray
        2D float image in [0, 1].
    method : {'otsu', 'mean'}, optional
        How to choose the threshold. Default is 'otsu'.
    sigma : float, optional
        Standard deviation of the Gaussian filter in pixels. Default is 2.
    post_process : bool, optional
        Whether to apply the morphological clean-up. Default is True.

    Returns
    -------
    np.ndarray
        2D bool array, True where lung was detected.
    """

    # smooth away pixel noise before thresholding
    smooth = filters.gaussian(image, sigma=sigma)

    # choose the threshold value
    if method == 'mean':
        t = smooth.mean()
    elif method == 'otsu':
        t = filters.threshold_otsu(smooth)
    else:
        raise ValueError("method must be 'mean' or 'otsu'")

    # dark pixels are candidate lung
    binary = smooth < t

    if not post_process:
        return binary

    # opening (erosion then dilation) removes specks and cuts thin bridges,
    # e.g. lungs joined to the outside air through the trachea
    binary = morphology.opening(binary, morphology.disk(5))

    # remove dark regions touching the image edge (air outside the body)
    binary = clear_border(binary)

    # keep the two largest regions, i.e. the two lungs
    binary = keep_largest_regions(binary, n=2)

    # fill holes fully enclosed by lung (vessels or ribs that came out bright)
    binary = ndi.binary_fill_holes(binary)

    # closing (dilation then erosion) smooths the outline and closes small gaps
    binary = morphology.closing(binary, morphology.disk(5))

    return binary


# ---------------------------------------------------------------------------
# Steps 7-8: assessment against the ground truth
# ---------------------------------------------------------------------------

def dice(pred, truth):

    """
    Dice coefficient between two binary masks, 2|A∩B| / (|A| + |B|).

    Parameters
    ----------
    pred : np.ndarray
        Predicted mask.
    truth : np.ndarray
        Ground-truth mask.

    Returns
    -------
    float
        1.0 for perfect overlap, 0.0 for no overlap.
    """

    pred, truth = pred.astype(bool), truth.astype(bool)

    overlap = np.logical_and(pred, truth).sum()
    total   = pred.sum() + truth.sum()

    # two empty masks agree perfectly
    return 2 * overlap / total if total > 0 else 1.0


def jaccard(pred, truth):

    """
    Jaccard index (intersection over union) between two binary masks, |A∩B| / |A∪B|.

    Parameters
    ----------
    pred : np.ndarray
        Predicted mask.
    truth : np.ndarray
        Ground-truth mask.

    Returns
    -------
    float
        1.0 for perfect overlap, 0.0 for no overlap.
    """

    pred, truth = pred.astype(bool), truth.astype(bool)

    union = np.logical_or(pred, truth).sum()

    # two empty masks agree perfectly
    return np.logical_and(pred, truth).sum() / union if union > 0 else 1.0


# ---------------------------------------------------------------------------
# Step 9: GLCM texture features
# ---------------------------------------------------------------------------

def glcm_features(image, mask, levels=32, distances=(1, 3, 5),
                  angles=(0, np.pi / 4, np.pi / 2, 3 * np.pi / 4)):

    """
    Compute GLCM texture features using only the pixels inside ``mask``.

    ``graycomatrix`` has no mask option, so lung intensities are quantised to
    grey levels 1 to ``levels - 1``, everything outside the lungs is set to 0,
    and row 0 / column 0 of the GLCM (every pair involving a non-lung pixel)
    is deleted before computing the properties. Each property is averaged
    over all distances and angles.

    Parameters
    ----------
    image : np.ndarray
        2D float image in [0, 1].
    mask : np.ndarray
        2D bool lung mask.
    levels : int, optional
        Number of grey levels including the background level 0. Default is 32.
    distances : tuple of int, optional
        Pixel offsets used for the co-occurrence counts.
    angles : tuple of float, optional
        Offset directions in radians.

    Returns
    -------
    dict
        One value per property in ``GLCM_PROPS``.
    """

    # rescale using lung pixels only, so overall exposure matters less
    lung   = image[mask]
    lo, hi = lung.min(), lung.max()
    scaled = np.clip((image - lo) / (hi - lo + 1e-8), 0, 1)

    # integer grey levels 1 .. levels-1, with 0 reserved for "not lung"
    quantised = (1 + np.round(scaled * (levels - 2))).astype(np.uint8)
    quantised[~mask] = 0

    # count grey-level pairs, shape (levels, levels, n_distances, n_angles)
    glcm = graycomatrix(quantised, distances=distances, angles=angles,
                        levels=levels, symmetric=True, normed=False)

    # drop all pairs involving the background level 0
    glcm = glcm[1:, 1:, :, :]

    # graycoprops normalises the matrix itself; average over distances and angles
    return {p: graycoprops(glcm, p).mean() for p in GLCM_PROPS}
