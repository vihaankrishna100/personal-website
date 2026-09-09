#!/usr/bin/env python3
"""
Rebuild the favicon set from photo.jpg.

Run this after swapping in a new photo:

    python3 make-favicon.py

If the new photo frames your face differently, adjust CENTER_X / CENTER_Y /
SIDE below — they describe a square, in pixels of photo.jpg, that gets cropped
out and turned into the icons. To find good numbers, open photo.jpg in Preview
and read the coordinates of the top of your hair and your chin.

Needs Pillow:  pip3 install pillow
"""

from PIL import Image, ImageDraw
import os

SOURCE = "photo.jpg"

# The square to crop, in source-image pixels.
CENTER_X = 132   # horizontal centre of the head
CENTER_Y = 122   # vertical centre of the head
SIDE     = 236   # width/height of the crop

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

src = Image.open(SOURCE).convert("RGB")
W, H = src.size

box = (CENTER_X - SIDE // 2, CENTER_Y - SIDE // 2,
       CENTER_X + SIDE // 2, CENTER_Y + SIDE // 2)
if box[0] < 0 or box[1] < 0 or box[2] > W or box[3] > H:
    raise SystemExit(
        f"Crop {box} falls outside the {W}x{H} image — "
        "lower SIDE or move CENTER_X / CENTER_Y.")

face = src.crop(box)


def circle(size):
    """Circular icon, supersampled so the edge stays smooth."""
    ss = size * 4
    im = face.resize((ss, ss), Image.LANCZOS)
    mask = Image.new("L", (ss, ss), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, ss - 1, ss - 1), fill=255)
    out = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out.resize((size, size), Image.LANCZOS)


circle(64).save("favicon.ico", format="ICO",
                sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
circle(32).save("favicon-32.png")
circle(192).save("favicon-192.png")
# iOS rounds the corners itself, so this one stays a filled square.
face.resize((180, 180), Image.LANCZOS).save("apple-touch-icon.png")

print(f"Cropped {box} from {SOURCE} ({W}x{H})")
print("Wrote favicon.ico, favicon-32.png, favicon-192.png, apple-touch-icon.png")
