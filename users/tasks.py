from celery import shared_task
from jelly_backend.one_signal.notification_service import send_email_via_onesignal
from jelly_backend.docs.onesignal import templates_ids


@shared_task(name='send_activate_account_email')
def send_activate_account_email(
        email: str,
        full_name: str,
        activate_account_code: str
):
    send_email_via_onesignal(
        email=email,
        template_id=templates_ids['EMAIL']['ACTIVATE_ACCOUNT'],
        full_name=full_name,
        activate_account_code=activate_account_code
    )
