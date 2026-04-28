"""
Main processing dispatcher.
Routes images to the appropriate restoration module based on type.
"""

import cv2
from .denoise import denoise_image
from .deblur import deblur_image
from .super_resolution import super_resolve_image


def process_image(input_path, output_path, restoration_type):
    """
    Load an image, apply the selected restoration, and save the result.
    Returns the method name used for processing.
    """
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Could not read the input image. The file may be corrupted.")

    if restoration_type == 'denoise':
        result, method = denoise_image(img)
    elif restoration_type == 'deblur':
        result, method = deblur_image(img)
    elif restoration_type == 'super_resolution':
        result, method = super_resolve_image(img)
    else:
        raise ValueError(f"Unknown restoration type: {restoration_type}")

    cv2.imwrite(output_path, result)
    return method
