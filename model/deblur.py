"""
Image Deblurring Module.
Implements Wiener deconvolution and unsharp masking for image deblurring.
"""

import cv2
import numpy as np


def deblur_image(img):
    """
    Apply deblurring pipeline using Wiener deconvolution + sharpening.
    Returns (result_image, method_name).
    """
    result = wiener_deblur(img)
    return result, "Wiener Deconvolution + Unsharp Mask"


def wiener_deblur(img, kernel_size=5, noise_var=0.01):
    """
    Wiener deconvolution-based deblurring.
    Assumes a simple motion blur kernel and applies frequency-domain filtering.
    """
    img_float = img.astype(np.float64) / 255.0

    result_channels = []
    for c in range(img_float.shape[2]):
        channel = img_float[:, :, c]
        deblurred = _wiener_channel(channel, kernel_size, noise_var)
        result_channels.append(deblurred)

    result = np.stack(result_channels, axis=2)
    result = np.clip(result * 255, 0, 255).astype(np.uint8)

    # Apply unsharp masking for additional sharpness
    result = unsharp_mask(result)

    return result


def _wiener_channel(channel, kernel_size=5, noise_var=0.01):
    """Apply Wiener deconvolution to a single channel."""
    # Create a simple motion blur kernel
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[kernel_size // 2, :] = 1.0 / kernel_size

    # Pad kernel to image size
    kernel_padded = np.zeros_like(channel)
    kh, kw = kernel.shape
    kernel_padded[:kh, :kw] = kernel

    # FFT of image and kernel
    img_fft = np.fft.fft2(channel)
    kernel_fft = np.fft.fft2(kernel_padded)

    # Wiener filter: H* / (|H|^2 + NSR)
    kernel_conj = np.conj(kernel_fft)
    wiener = kernel_conj / (np.abs(kernel_fft) ** 2 + noise_var)

    # Apply filter and inverse FFT
    result_fft = img_fft * wiener
    result = np.real(np.fft.ifft2(result_fft))

    return np.clip(result, 0, 1)


def unsharp_mask(img, sigma=1.0, strength=1.5):
    """
    Unsharp masking: enhances edges by subtracting a blurred version.
    result = original + strength * (original - blurred)
    """
    blurred = cv2.GaussianBlur(img, (0, 0), sigma)
    sharpened = cv2.addWeighted(img, 1.0 + strength, blurred, -strength, 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)
