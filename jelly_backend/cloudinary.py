import cloudinary
import os


def configure_cloudinary():
    """
    Function to configure the Cloudinary SDK with the environment variables

    :return: None
    """
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    )
