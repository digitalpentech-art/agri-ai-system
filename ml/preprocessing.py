from PIL import Image
import numpy as np
from ml.config import IMG_SIZE

def preprocess_image(image_path):
    """
    Validates, opens, resizes, and normalizes an image for model inference.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize(IMG_SIZE)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        raise ValueError(f"Failed to preprocess image: {e}")
