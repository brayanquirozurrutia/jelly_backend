from functools import wraps
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from graphql import GraphQLError


def validate_token(func):
    @wraps(func)
    def wrapper(self, info, *args, **kwargs):
        # Leer cookies del contexto de la solicitud
        cookies = info.context.get('request', {}).COOKIES

        access_token = cookies.get('access_token')
        if not access_token:
            raise GraphQLError('Debes iniciar sesión')

        try:
            # Validar el token de acceso
            access_token_obj = AccessToken(access_token)
        except TokenError:
            raise GraphQLError('Token inválido')

        return func(self, info, *args, **kwargs)

    return wrapper
