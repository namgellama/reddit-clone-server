from fastapi import HTTPException, UploadFile, status
from starlette.concurrency import run_in_threadpool
import uuid
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

from app.config.env import settings

MEDIA_PATH = "media/posts"
MEDIA_DIR = Path(MEDIA_PATH)


class ImageService:
    MAX_IMAGES = settings.max_upload_length
    ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    MAX_SIZE = settings.max_upload_size_bytes

    @staticmethod
    def process_image(content: bytes) -> str:
        with Image.open(BytesIO(content)) as original:
            img = ImageOps.exif_transpose(original)

            img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")

            filename = f"{uuid.uuid4().hex}.jpg"
            filepath = MEDIA_DIR / filename

            MEDIA_DIR.mkdir(parents=True, exist_ok=True)

            img.save(filepath, "JPEG", quality=85, optimize=True)

        return f"/{MEDIA_PATH}/{filename}"

    @classmethod
    async def validate_and_process(cls, files: list[UploadFile]) -> list[str]:
        if len(files) > cls.MAX_IMAGES:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Maximum {cls.MAX_IMAGES} images allowed",
            )

        image_list = []

        for file in files:
            # Validate type
            if file.content_type not in cls.ALLOWED_TYPES:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, f"{file.filename}: unsupported type"
                )

            # Validate size
            file_bytes = await file.read()
            if len(file_bytes) > cls.MAX_SIZE:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, f"{file.filename}: file too large"
                )

            # Process image
            try:
                filename = await run_in_threadpool(cls.process_image, file_bytes)
                image_list.append(filename)
            except UnidentifiedImageError:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, f"{file.filename}: invalid image"
                )

        return image_list

    @staticmethod
    def delete_image(filename: str | None) -> None:
        if not filename:
            return

        filename = filename.lstrip("/")

        filepath = Path.cwd() / filename

        if filepath.exists():
            filepath.unlink()
