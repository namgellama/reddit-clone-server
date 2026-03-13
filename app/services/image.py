from fastapi import HTTPException, UploadFile, status
from starlette.concurrency import run_in_threadpool
from PIL import UnidentifiedImageError

from app.config.env import settings
from app.utils.image import process_image


class ImageService:
    MAX_IMAGES = settings.max_upload_length
    ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    MAX_SIZE = settings.max_upload_size_bytes

    @staticmethod
    async def validate_and_process(files: list[UploadFile]) -> list[str]:
        if len(files) > ImageService.MAX_IMAGES:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Maximum {ImageService.MAX_IMAGES} images allowed",
            )

        image_list = []

        for file in files:
            # Validate type
            if file.content_type not in ImageService.ALLOWED_TYPES:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, f"{file.filename}: unsupported type"
                )

            # Validate size
            file_bytes = await file.read()
            if len(file_bytes) > ImageService.MAX_SIZE:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, f"{file.filename}: file too large"
                )

            # Process image
            try:
                filename = await run_in_threadpool(process_image, file_bytes)
                image_list.append(filename)
            except UnidentifiedImageError:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, f"{file.filename}: invalid image"
                )

        return image_list
