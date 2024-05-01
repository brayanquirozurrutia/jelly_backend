from rest_framework import serializers

from jelly_backend.utils import valida_rut
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password_2 = serializers.CharField(required=True, write_only=True)
    rut = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    gender = serializers.ChoiceField(required=True, choices=['M', 'F', 'O'])
    birth_date = serializers.DateField(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'rut',
            'first_name',
            'last_name',
            'email',
            'password',
            'gender',
            'birth_date',
            'password_2',
        ]

        read_only_fields = [
            'id',
        ]

    # We clean the data before
    @staticmethod
    def validate_rut(rut):
        return rut.strip()

    @staticmethod
    def validate_first_name(first_name):
        return first_name.lower().strip().capitalize()

    @staticmethod
    def validate_last_name(last_name):
        return last_name.lower().strip().capitalize()

    @staticmethod
    def validate_email(email):
        return email.lower().strip()

    @staticmethod
    def validate_password(password):
        return password.strip()

    @staticmethod
    def validate_gender(gender):
        return gender.upper().strip()

    @staticmethod
    def validate_password_2(password_2):
        return password_2.strip()

    # We validate the data
    def validate(self, data):
        # We verify that the email is unique
        email = data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("El email ya está en uso.")
        rut = data['rut']
        # We verify that the RUT is valid
        if not valida_rut(rut):
            raise serializers.ValidationError("El RUT no es válido.")
        # We verify that the RUT is unique
        if User.objects.filter(rut=rut).exists():
            raise serializers.ValidationError("El RUT ya está en uso.")
        # We verify that the passwords match
        if data['password'] != data['password_2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    # We create the user
    def create(self, validated_data):
        validated_data.pop('password_2')
        user = User.objects.create_user(**validated_data)
        return user
