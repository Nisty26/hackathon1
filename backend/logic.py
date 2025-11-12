from typing import Tuple, List, Dict
from color_utils import hue_diff

def classify_undertone(rgb: Tuple[int, int, int]) -> str:
    """Classify undertone based on R/B balance and subtle logic."""
    r, g, b = rgb

    # Warm: red/orange/yellow tones dominate
    if r > b + 25 and g > b:
        return "Warm"

    # Cool: blue/pink tones dominate
    elif b > r + 25:
        return "Cool"

    # Neutral: balanced tones
    else:
        return "Neutral"


def harmony_type(hue1: float, hue2: float) -> str:
    """Classify outfit harmony type."""
    d = hue_diff(hue1, hue2)

    if abs(d - 180) <= 15:
        return "Complementary"
    elif d <= 30:
        return "Analogous"
    elif 30 < d < 100:
        return "Balanced Contrast"
    else:
        return "Clashing"


PALETTES: Dict[str, List[str]] = {
    "Warm":    ["Olive", "Coral", "Mustard", "Cream", "Red-Orange"],
    "Cool":    ["Navy", "Rose", "Emerald", "Gray", "Lavender"],
    "Neutral": ["Beige", "White", "Teal", "Charcoal", "Soft Pink"],
}
