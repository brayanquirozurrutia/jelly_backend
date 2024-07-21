from functools import wraps
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from graphql import GraphQLError


def validate_token(func):
    @wraps(func)
    def wrapper(self, info, *args, **kwargs):
        # Obtener la solicitud del contexto
        request = info.context.get('request')
        if request is None:
            raise GraphQLError('No se pudo obtener la solicitud.')

        # Leer las cookies de la solicitud
        cookies = request.COOKIES

        # Obtener el token de acceso desde las cookies
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
