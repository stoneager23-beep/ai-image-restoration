"""
Super Resolution Module.
Implements bicubic upscaling with detail enhancement and edge-aware sharpening.
"""

import cv2
import numpy as np


def super_resolve_image(img, scale=2):
    """
    Enhance image resolution by the given scale factor.
    Uses bicubic interpolation + bilateral filtering + detail enhancement.
    Returns (result_image, method_name).
    """
    result = enhanced_upscale(img, scale)
    return result, f"Enhanced Bicubic Upscale ({scale}x)"


def enhanced_upscale(img, scale=2):
    """
    Multi-step super resolution pipeline:
    1. Bicubic interpolation for upscaling
    2. Bilateral filter for edge-preserving smoothing
    3. Unsharp masking for detail enhancement
    4. Detail enhancement for texture recovery
    """
    h, w = img.shape[:2]

    # Step 1: Bicubic upscale
    upscaled = cv2.resize(
        img, (w * scale, h * scale),
        interpolation=cv2.INTER_CUBIC
    )

    # Step 2: Bilateral filter (smooth while preserving edges)
    smoothed = cv2.bilateralFilter(upscaled, 9, 75, 75)

    # Step 3: Unsharp masking
    gaussian = cv2.GaussianBlur(smoothed, (0, 0), 3)
    sharpened = cv2.addWeighted(smoothed, 1.5, gaussian, -0.5, 0)

    # Step 4: Detail enhancement
    detail_enhanced = cv2.detailEnhance(sharpened, sigma_s=10, sigma_r=0.15)

    return detail_enhanced
