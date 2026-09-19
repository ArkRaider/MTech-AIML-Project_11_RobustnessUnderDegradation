import torch
import torchvision.transforms.functional as F
from PIL import Image, ImageFilter
import numpy as np

def apply_blur(image, severity):
    if severity == 0: return image
    radius = severity * 1.0 # Radius increases by 1 per severity
    return image.filter(ImageFilter.GaussianBlur(radius))

def apply_noise(image, severity):
    if severity == 0: return image
    img_array = np.array(image).astype(np.float32)
    std = severity * 10.0 # Standard deviation increases by 10 per severity
    noise = np.random.normal(0, std, img_array.shape)
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img)

def apply_brightness(image, severity):
    if severity == 0: return image
    # Decrease brightness progressively
    factor = max(0.1, 1.0 - severity * 0.15)
    return F.adjust_brightness(image, factor)

def apply_rotation(image, severity):
    if severity == 0: return image
    # Rotate by increasing angle
    angle = severity * 15
    return F.rotate(image, angle)

def get_degradations():
    return {
        'blur': apply_blur,
        'noise': apply_noise,
        'brightness': apply_brightness,
        'rotation': apply_rotation
    }
