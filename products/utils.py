import cloudinary
import cloudinary.uploader
from io import BytesIO
from PIL import Image


def upload_image_to_cloudinary(
        image_file: BytesIO,
        folder: str,
) -> str:
    """
    Function to upload an image to Cloudinary

    :param image_file: BytesIO object containing the image to upload
    :param folder: Folder in which to store the image
    :return: URL of the uploaded image
    """
    try:
        # Open and process the image using Pillow
        image = Image.open(image_file)
        buffer = BytesIO()
        image.save(buffer, format='WEBP', optimize=True, quality=100)
        buffer.seek(0)

        uploaded_image = cloudinary.uploader.upload(
            file=buffer,
            folder=folder,
            overwrite=True,
            resource_type="image"
        )
        return uploaded_image['secure_url']
    except cloudinary.exceptions.Error:
        raise ValueError(f"Cloudinary error")
    except Exception:
        raise ValueError(f"Error uploading image to Cloudinary")
