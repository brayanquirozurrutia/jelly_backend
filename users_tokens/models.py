from django.db import models
import uuid
from django.utils import timezone
import random
from users.models import User


class AccountActivationToken(models.Model):
    """
    Model for storing account activation tokens
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, blank=False, null=False, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_activation_token",
                                related_query_name="account_activation_token")
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(blank=False, null=False, unique=True, default="000000", max_length=6)

    class Meta:
        db_table = "account_activation_token"

    def save(self, *args, **kwargs):
        while True:
            random_code = str(random.randint(100000, 999999))
            if not AccountActivationToken.objects.filter(code=random_code).exists():
                self.code = random_code
                break
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        expiration_time = timezone.timedelta(minutes=15)
        return self.created_at + expiration_time < timezone.now()

    @classmethod
    def create_new_token(cls, user: User) -> "AccountActivationToken":
        # Delete the existing token if there is one associated with the user
        cls.objects.filter(user=user).delete()
        # Create a new token for the given user
        new_token = cls.objects.create(user=user)
        return new_token
