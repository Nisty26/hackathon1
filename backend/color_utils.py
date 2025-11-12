from io import BytesIO
from PIL import Image
import colorsys
import numpy as np

def load_image(file_bytes: bytes) -> Image.Image:
    img = Image.open(BytesIO(file_bytes)).convert("RGB")
    return img

def dominant_rgb(file_bytes: bytes) -> tuple[int, int, int]:
    """Deterministic version — uses pixel averaging instead of random sampling."""
    img = load_image(file_bytes)
    img = img.resize((100, 100))  # normalize image size for consistency
    arr = np.array(img)
    mean_color = arr.reshape(-1, 3).mean(axis=0)
    r, g, b = [int(v) for v in mean_color]
    return (r, g, b)

def rgb_to_hsv_deg(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    r, g, b = [v/255.0 for v in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (h*360.0, s*100.0, v*100.0)

def hue_diff(h1: float, h2: float) -> float:
    d = abs(h1 - h2) % 360.0
    return min(d, 360.0 - d)
