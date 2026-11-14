# Converts the three existing Ugo identity artworks into clean transparent PNG assets.
from pathlib import Path
from PIL import Image, ImageFilter
from rembg import remove, new_session

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "FF7953C1-7062-44DD-A20C-FFF25918A014.jpeg",
    "ugo-identidade-vertical.jpg",
    "ugo-personagem-e-logo.jpg",
]
session = new_session("u2net")
for name in FILES:
    source = ROOT / name
    if not source.exists():
        raise FileNotFoundError(source)
    image = Image.open(source).convert("RGBA")
    result = remove(
        image,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=8,
    ).convert("RGBA")
    alpha = result.getchannel("A").point(lambda value: 0 if value < 190 else min(255, int((value - 190) * 3.92)))
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.45))
    result.putalpha(alpha)
    result.save(ROOT / (source.stem + ".png"), format="PNG", optimize=True)
    print(f"Created clean transparent PNG: {source.stem}.png")
