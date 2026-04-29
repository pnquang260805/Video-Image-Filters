import cv2
import numpy as np
from services.filters import blur
from PIL import Image

def test_blur_numpy():
    print("Testing blur with numpy array...")
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(img, (20, 20), (80, 80), (255, 255, 255), -1)
    blurred = blur(img)
    assert blurred.shape == img.shape
    assert not np.array_equal(img, blurred)
    print("Numpy blur test passed!")

def test_blur_pil():
    print("Testing blur with PIL Image...")
    img_pil = Image.new('RGB', (100, 100), color='black')
    img_np = np.array(img_pil)
    blurred = blur(img_pil)
    assert isinstance(blurred, np.ndarray)
    assert blurred.shape == (100, 100, 3)
    print("PIL blur test passed!")

if __name__ == "__main__":
    test_blur_numpy()
    test_blur_pil()
    print("All tests passed!")
