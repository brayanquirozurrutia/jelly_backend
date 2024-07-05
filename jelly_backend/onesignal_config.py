import onesignal
import os
from dotenv import load_dotenv

load_dotenv()

configuration = onesignal.Configuration(
    app_key=os.getenv("ONESIGNAL_API_KEY"),
    user_key=None,
)


def get_onesignal_client():
    return onesignal.ApiClient(configuration)
