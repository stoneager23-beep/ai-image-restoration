"""
Noise Removal Module.
Implements Gaussian filter, Median filter, and Non-Local Means denoising.
Includes DnCNN PyTorch model for AI-based denoising.
"""

import cv2
import numpy as np
from .dncnn import denoise_with_dncnn


def denoise_image(img):
    """
    Apply multi-stage noise removal pipeline.
    Tries DnCNN first, falls back to classical OpenCV methods.
    Returns (result_image, method_name).
    """
    # Try AI-based denoising first
    try:
        result = denoise_with_dncnn(img)
        if result is not None:
            return result, "DnCNN (AI-based)"
    except Exception:
        pass

    # Classical pipeline fallback
    result = classical_denoise(img)
    return result, "NL-Means + Median Filter (Classical)"


def classical_denoise(img):
    """
    Classical denoising pipeline:
    1. Median filter to remove salt-and-pepper noise
    2. Non-Local Means for Gaussian noise removal
    """
    # Step 1: Median filter (excellent for impulse noise)
    median_filtered = cv2.medianBlur(img, 3)

    # Step 2: Non-Local Means Denoising (state-of-the-art classical method)
    # Using positional args for OpenCV 4.13+ compatibility
    denoised = cv2.fastNlMeansDenoisingColored(
        median_filtered,  # src
        None,             # dst
        10,               # h (filter strength for luminance)
        10,               # hForColorComponents
        7,                # templateWindowSize
        21                # searchWindowSize
    )

    return denoised


def gaussian_denoise(img, kernel_size=5):
    """Simple Gaussian blur denoising."""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def median_denoise(img, kernel_size=5):
    """Median filter denoising (good for salt-and-pepper noise)."""
    return cv2.medianBlur(img, kernel_size)
