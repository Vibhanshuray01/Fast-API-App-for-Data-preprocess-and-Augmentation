# image_augmentation.py
from PIL import Image, ImageEnhance

def augment_image(image: Image) -> Image:
    """Rotate the image and enhance brightness."""
    rotated_img = image.rotate(45)
    enhancer = ImageEnhance.Brightness(rotated_img)
    enhanced_img = enhancer.enhance(1.5)  # Increase brightness
    return enhanced_img
