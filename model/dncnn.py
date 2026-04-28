"""
DnCNN (Denoising Convolutional Neural Network) Module.
Implements the DnCNN architecture in PyTorch for AI-based image denoising.
Falls back to OpenCV NL-Means if pretrained weights are not available.

Reference: Zhang et al., "Beyond a Gaussian Denoiser: Residual Learning
of Deep CNN for Image Denoising", IEEE TIP 2017.
"""

import os
import cv2
import numpy as np

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class DnCNN(object):
    """
    DnCNN model architecture.
    Uses residual learning: the network predicts the noise,
    and the clean image = noisy image - predicted noise.
    """

    def __init__(self, channels=1, num_layers=17, features=64):
        if not TORCH_AVAILABLE:
            return

        import torch.nn as nn

        layers = []
        # First layer: Conv + ReLU
        layers.append(nn.Conv2d(channels, features, kernel_size=3, padding=1, bias=False))
        layers.append(nn.ReLU(inplace=True))

        # Middle layers: Conv + BatchNorm + ReLU
        for _ in range(num_layers - 2):
            layers.append(nn.Conv2d(features, features, kernel_size=3, padding=1, bias=False))
            layers.append(nn.BatchNorm2d(features))
            layers.append(nn.ReLU(inplace=True))

        # Last layer: Conv (outputs noise estimate)
        layers.append(nn.Conv2d(features, channels, kernel_size=3, padding=1, bias=False))

        self.model = nn.Sequential(*layers)

    def to(self, device):
        if TORCH_AVAILABLE:
            self.model = self.model.to(device)
        return self

    def eval(self):
        if TORCH_AVAILABLE:
            self.model.eval()
        return self

    def load_state_dict(self, state_dict):
        if TORCH_AVAILABLE:
            self.model.load_state_dict(state_dict)

    def __call__(self, x):
        if TORCH_AVAILABLE:
            noise = self.model(x)
            return x - noise  # Residual learning
        return x


def denoise_with_dncnn(img, weights_path=None):
    """
    Denoise an image using the DnCNN model.

    Args:
        img: BGR image (numpy array)
        weights_path: path to pretrained weights (.pth file)

    Returns:
        Denoised image or None if model/weights unavailable.
    """
    if not TORCH_AVAILABLE:
        return None

    # Look for weights in the model directory
    if weights_path is None:
        model_dir = os.path.dirname(__file__)
        weights_path = os.path.join(model_dir, 'weights', 'dncnn.pth')

    if not os.path.exists(weights_path):
        # No pretrained weights available — return None to trigger fallback
        return None

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = DnCNN(channels=1, num_layers=17, features=64).to(device)
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.eval()

    # Convert to grayscale and normalize
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_norm = gray.astype(np.float32) / 255.0

    # Create tensor: (1, 1, H, W)
    tensor = torch.from_numpy(gray_norm).unsqueeze(0).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(tensor)

    # Convert back to numpy
    output_np = output.squeeze().cpu().numpy()
    output_np = np.clip(output_np * 255, 0, 255).astype(np.uint8)

    # Apply the denoised luminance to the color image (preserve color)
    img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    img_ycrcb[:, :, 0] = output_np
    result = cv2.cvtColor(img_ycrcb, cv2.COLOR_YCrCb2BGR)

    return result
