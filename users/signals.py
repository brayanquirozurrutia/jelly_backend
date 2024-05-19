from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from users_tokens.models import AccountActivationToken


@receiver(post_save, sender=User)
def create_account_activation_token(sender, instance, created, **kwargs):
    if created:
        AccountActivationToken.objects.create(user=instance)
