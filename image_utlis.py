import uuid # generating unique filenames
from io import BytesIO # image bytes and memory
from pathlib import Path # for file operations, more modern, instad of just string manipulations

from PIL import Image, ImageOps # main image functionality, cpu bound work so not good for async,
# so we write a sync func, use threadpool which will offload it to a separate thread

PROFILE_PICS_DIR = Path("media/profile_pics")

def preprocess_profile_image(content: bytes) -> str:
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original) # right orientation
        img = ImageOps.fit(img, (300,300), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "P","LA"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = PROFILE_PICS_DIR/filename

        PROFILE_PICS_DIR.mkdir(parents=True, exist_ok=True)
        img.save(filepath, "JPEG", quality=85, optimize=True)

    return filename

def delete_profile_image(filename: str | None) -> None:
    if filename is None:
        return

    filepath = PROFILE_PICS_DIR/filename
    if filepath.exists():
        filepath.unlink()

