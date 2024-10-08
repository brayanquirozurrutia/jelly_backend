from celery import shared_task
from jelly_backend.one_signal.notification_service import send_email_via_onesignal
from jelly_backend.docs.onesignal import templates_ids


@shared_task(name='send_account_activated_email')
def send_account_activated_email(
        email: str,
        full_name: str,
):
    send_email_via_onesignal(
        email=email,
        template_id=templates_ids['EMAIL']['ACCOUNT_ACTIVATED'],
        full_name=full_name,
    )


@shared_task(name='send_welcome_email')
def send_welcome_email(
        email: str,
        full_name: str,
):
    send_email_via_onesignal(
        email=email,
        template_id=templates_ids['EMAIL']['WELCOME'],
        full_name=full_name,
    )


@shared_task(name='send_new_account_activation_token_email')
def send_new_account_activation_token_email(
        email: str,
        full_name: str,
        activate_account_code: str,
):
    send_email_via_onesignal(
        email=email,
        template_id=templates_ids['EMAIL']['ACTIVATE_ACCOUNT'],
        full_name=full_name,
        activate_account_code=activate_account_code,
    )


@shared_task(name='send_forgot_password_email')
def send_forgot_password_email(
        email: str,
        full_name: str,
        reset_password_code: str,
):
    send_email_via_onesignal(
        email=email,
        template_id=templates_ids['EMAIL']['FORGOT_PASSWORD'],
        full_name=full_name,
        reset_password_code=reset_password_code,
    )


@shared_task(name='send_password_changed_email')
def send_password_changed_email(
        email: str,
        full_name: str,
):
    send_email_via_onesignal(
        email=email,
        template_id=templates_ids['EMAIL']['PASSWORD_CHANGED'],
        full_name=full_name,
    )
