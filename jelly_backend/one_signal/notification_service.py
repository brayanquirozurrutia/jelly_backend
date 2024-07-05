import os
from dotenv import load_dotenv

import onesignal
from onesignal.api import default_api
from onesignal.model.notification import Notification
from onesignal.model.player import Player

from jelly_backend.onesignal_config import get_onesignal_client

load_dotenv()


def create_onesignal_user(
        email: str,
        full_name: str,
        device_type: int = 11
) -> None:
    """
    Creates a new user in OneSignal.
    :param email: The email of the user.
    :param full_name: The full name of the user.
    :param device_type: The device type of the user.
    :return: None
    """
    api_client = get_onesignal_client()
    api_instance = default_api.DefaultApi(api_client)

    player = Player(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        device_type=device_type,
        email=email,
        tags={
            "full_name": full_name,
        }
    )

    try:
        response = api_instance.create_player(player)
        print(f"User created: {response}")
    except onesignal.ApiException as e:
        print(f"Exception when calling DefaultApi->create_player: {e}")


def send_email_via_onesignal(
        email: str,
        template_id: str,
        full_name: str,
        activate_account_code: str = '000000',
        reset_password_code: str = '000000'
) -> None:
    """
    Sends an email via OneSignal.
    :param email: The email of the user.
    :param template_id: The template id.
    :param full_name: The full name of the user.
    :param activate_account_code: The account activation code for the user.
    :param reset_password_code: The reset password code for the user.
    :return: None
    """
    api_client = get_onesignal_client()
    api_instance = default_api.DefaultApi(api_client)

    notification = Notification(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        template_id=template_id,
        include_email_tokens=[email],
        custom_data={
            "full_name": full_name,
            "activate_account_code": activate_account_code,
            "reset_password_code": reset_password_code
        }
    )

    try:
        api_instance.create_notification(notification)
    except onesignal.ApiException as e:
        print(f"Exception when calling DefaultApi->create_notification: {e}")
