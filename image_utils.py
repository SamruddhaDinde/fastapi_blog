import uuid # generating unique filenames
from io import BytesIO # image bytes and memory
#from pathlib import Path # for file operations, more modern, instad of just string manipulations
import boto3
from config import settings
from starlette.concurrency import run_in_threadpool

from PIL import Image, ImageOps # main image functionality, cpu bound work so not good for async,
# so we write a sync func, use threadpool which will offload it to a separate thread

def _get_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.s3_region,
        aws_access_key_id=(
            settings.s3_access_key_id.get_secret_value()
            if settings.s3_access_key_id
            else None
        ),
        aws_secret_access_key=(
            settings.s3_secret_access_key.get_secret_value()
            if settings.s3_secret_access_key
            else None
        ),
        endpoint_url = settings.s3_endpoint_url
    )


def preprocess_profile_image(content: bytes) -> tuple[bytes, str]:
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original) # right orientation
        img = ImageOps.fit(img, (300,300), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "P","LA"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"
        output = BytesIO()

        img.save(output, "JPEG", quality=85, optimize=True)
        output.seek(0)

    return output.read(), filename

# def delete_profile_image(filename: str | None) -> None:
#     if filename is None:
#         return

#     filepath = PROFILE_PICS_DIR/filename
#     if filepath.exists():
#         filepath.unlink()

def _upload_to_s3(file_bytes: bytes, key: str) -> None:
    s3 = _get_s3_client()
    s3.upload_fileobj(
        BytesIO(file_bytes),
        settings.s3_bucket_name,
        key,
        ExtraArgs={"ContentType":"image/jpeg"},
    )

def _delete_from_s3(key:str)-> None:
    s3 = _get_s3_client()
    s3.delete_object(Bucket=settings.s3_bucket_name, Key=key)

# boto3 calls are blocking, not async
# so we offload it to threadpool through run_in_threadpool, for any blocking library in async app

async def upload_profile_image(file_bytes: bytes, filename: str) -> None:
    key = f"profile-pics/{filename}"
    await run_in_threadpool(_upload_to_s3, file_bytes, key)

async def delete_profile_image(filename: str | None) -> None:
    if filename is None:
        return
    key = f"profile-pics/{filename}"
    await run_in_threadpool(_delete_from_s3, key)
    
