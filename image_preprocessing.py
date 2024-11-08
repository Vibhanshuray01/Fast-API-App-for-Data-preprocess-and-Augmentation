# image_preprocessing.py
from PIL import Image

def preprocess_image(image: Image) -> Image:
    """Convert image to grayscale."""
    return image.convert("L")

