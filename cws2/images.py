from io import BytesIO

from django.core.files import File
from PIL import Image, ImageOps


def _convert_image_to_webp(image_file, thumbnail_size=(486, 486)):
    """Private helper function for image conversion."""
    image = (
        image_file if isinstance(image_file, Image.Image) else Image.open(image_file)
    )
    ImageOps.exif_transpose(image, in_place=True)
    image.convert("RGB")
    image.thumbnail(thumbnail_size)
    thumb_io = BytesIO()
    image.save(thumb_io, "WEBP")
    return File(thumb_io, name=image_file.name)


def process_avatar_image(image_file):
    """Image conversion function for user avatars."""
    return _convert_image_to_webp(image_file)


def process_flag_image(image_file):
    """Image conversion function for language flags."""
    return _convert_image_to_webp(image_file, thumbnail_size=(100, 100))
