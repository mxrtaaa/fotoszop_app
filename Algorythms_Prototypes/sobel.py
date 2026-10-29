from __future__ import annotations
import numpy as np
from dataclasses import dataclass

Sobel_x = np.array([[1, 0, -1],
                    [2, 0, -2],
                    [1, 0, -1]], dtype=np.float64)

Sobel_y = np.array([[1, 2, 1],
                    [0, 0, 0],
                    [-1, -2, -1]], dtype=np.float64)
def to_gray(image: np.ndarray) -> np.ndarray:
    # Jeśli obraz jest już w skali szarości (2D)
    if len(image.shape) == 2:
        return image.astype(np.float64)
    
    # Jeśli obraz ma 3 kanały (RGB) lub 4 kanały (RGBA - usuwamy kanał alfa)
    elif len(image.shape) == 3:
        if image.shape[2] == 4:
            image = image[..., :3]  # Odrzucamy kanał przezroczystości
        if image.shape[2] == 3:
            return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
            
    raise ValueError(f"Nieobsługiwany kształt obrazu: {image.shape}. Wymagane RGB lub skala szarości.")
def correlate2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    kernel_height, kernel_width = kernel.shape
    image_height, image_width = image.shape

    # Calculate the padding size
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    # Pad the image with zeros
    padded_image = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')

    # Prepare an output array
    output = np.zeros_like(image)

    # Perform correlation
    for i in range(image_height):
        for j in range(image_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            output[i, j] = np.sum(region * kernel)

    return output
def convolve2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    # Flip the kernel for convolution
    flipped_kernel = np.flipud(np.fliplr(kernel))
    return correlate2d(image, flipped_kernel)
@dataclass
class SobelResult:
    gx: np.ndarray
    gy: np.ndarray
    magnitude: np.ndarray
    direction: np.ndarray
def sobell(image, pad_mode="edge") -> SobelResult:
    gray_image = to_gray(image)

    # Compute gradients
    gx = convolve2d(gray_image, Sobel_x)
    gy = convolve2d(gray_image, Sobel_y)

    # Compute magnitude and direction
    magnitude=np.hypot(gx, gy)
    direction = np.arctan2(gy, gx)

    return SobelResult(gx=gx, gy=gy, magnitude=magnitude, direction=direction)
def edge_map(image: np.ndarray, threshold: float) -> np.ndarray:
    sobel_result = sobell(image)
    magnitude = sobel_result.magnitude

    # Create an edge map based on the threshold
    edge_map = (magnitude > threshold).astype(np.uint8) * 255

    return edge_map
