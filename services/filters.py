from PIL.Image import Image
import cv2
import numpy as np

def blur(image, ksize=(15, 15)):
    """
    Applies a blur filter to the image.
    Supports both PIL Image and numpy ndarray.
    """
    if not isinstance(image, np.ndarray):
        # Assume it's a PIL Image or similar
        image = np.array(image)
    
    return cv2.blur(image, ksize)
