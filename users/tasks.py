from celery import shared_task
from jelly_backend.one_signal.notification_service import send_email_via_onesignal


@shared_task(name='send_one_signal_email')
def send_one_signal_email(
        email: str,
        template_id: str,
        full_name: str,
        activate_account_code: str
):
    send_email_via_onesignal(
        email=email,
        template_id=template_id,
        full_name=full_name,
        activate_account_code=activate_account_code
    )
