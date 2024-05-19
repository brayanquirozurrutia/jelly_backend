from django.db import transaction
from rest_framework import serializers
from users_tokens.models import AccountActivationToken
from users.models import User


class AccountActivationTokenActivateAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for activating the account with the token
    """
    account_activation_token = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = AccountActivationToken
        fields = [
            'account_activation_token',
            'email',
        ]

    # We clean the data before
    @staticmethod
    def validate_email(email):
        return email.lower().strip()

    @staticmethod
    def validate_account_activation_token(account_activation_token):
        return account_activation_token.strip()

    # We validate the token
    def validate(self, attrs):
        account_activation_token = attrs['account_activation_token']
        email = attrs['email']
        # We verify that the token is valid and that it is associated with the email
        account_activation_token_obj = AccountActivationToken.objects.filter(
            code=account_activation_token,
            user__email=email
        ).first()
        if not account_activation_token_obj:
            raise serializers.ValidationError("El token no es válido.")
        # We verify that the token has not expired
        if account_activation_token_obj.is_expired:
            raise serializers.ValidationError("El token ha expirado.")
        # We verify that the user is not already active
        if account_activation_token_obj.user.user_status != 'R':
            raise serializers.ValidationError("La cuenta ya ha sido activada.")
        return attrs

    def save(self, **kwargs):
        # We activate the account and delete the token associated with it
        account_activation_token = self.validated_data['account_activation_token']
        email = self.validated_data['email']
        try:
            account_activation_token_obj = AccountActivationToken.objects.get(
                code=account_activation_token,
                user__email=email
            )
            with transaction.atomic():
                account_activation_token_obj.user.user_status = 'A'
                account_activation_token_obj.user.save()
                account_activation_token_obj.delete()
            self.instance = account_activation_token_obj
            return account_activation_token_obj
        except AccountActivationToken.DoesNotExist:
            self.instance = None
            return None


class AccountActivationTokenNewTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new account activation token
    New token is created when only if the user exists and is registered
    """
    email = serializers.EmailField(required=True)

    class Meta:
        model = AccountActivationToken
        fields = [
            'email',
        ]

    # We clean the data before
    @staticmethod
    def validate_email(email):
        return email.lower().strip()

    def save(self, **kwargs):
        email = self.validated_data['email']
        user_obj = User.objects.filter(email=email).first()
        if user_obj:
            user_status = user_obj.user_status
            if user_status == 'R':
                with transaction.atomic():
                    # We create a new token
                    account_activation_token_obj = AccountActivationToken.create_new_token(
                        user=user_obj
                    )
                    self.instance = account_activation_token_obj
                    return account_activation_token_obj
        self.instance = None
        return None
