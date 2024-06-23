from datetime import datetime
from rest_framework import serializers
from dateutil.relativedelta import relativedelta
from jelly_backend.utils.utils import valida_rut
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
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
            'nickname',
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
        return first_name.strip().capitalize()

    @staticmethod
    def validate_last_name(last_name):
        return last_name.strip().capitalize()

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

    @staticmethod
    def validate_nickname(nickname):
        return nickname.strip().capitalize()

    # We validate the data
    def validate(self, attrs):
        # We verify that the email is unique
        email = attrs['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("El email ya está en uso.")
        rut = attrs['rut']
        # We verify that the RUT is valid
        if not valida_rut(rut):
            raise serializers.ValidationError("El RUT no es válido.")
        # We verify that the RUT is unique
        if User.objects.filter(rut=rut).exists():
            raise serializers.ValidationError("El RUT ya está en uso.")
        # We verify that the passwords match
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        # We verify that the user is of legal age
        birth_date = attrs['birth_date']
        age = relativedelta(datetime.now(), birth_date).years
        if age < 15:
            raise serializers.ValidationError("Debes ser mayor de edad para registrarte.")
        # We verify that the age is not greater than 100
        if age > 100:
            raise serializers.ValidationError("Debes ingresar una edad válida.")
        return attrs

    # We create the user
    def create(self, validated_data):
        validated_data.pop('password_2')
        user = User.objects.create_user(**validated_data)
        self.instance = user
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for the login of the User model.
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
        ]

    @staticmethod
    def validate_email(email):
        return email.lower().strip()

    @staticmethod
    def validate_password(password):
        return password.strip()

    # We validate the data
    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("El email o la contraseña son incorrectos.")
        if not user.check_password(password):
            raise serializers.ValidationError("El email o la contraseña son incorrectos.")
        # We check if the user is active
        if user.user_status != 'A':
            raise serializers.ValidationError("El usuario no está activo.")
        self.instance = user
        return attrs

    def save(self, **kwargs):
        user = self.instance
        user.last_login = datetime.now()
        user.save()
        self.instance = user
        return user
