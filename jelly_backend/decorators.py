from functools import wraps
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from graphql import GraphQLError


def validate_token(func):
    @wraps(func)
    def wrapper(self, info, *args, **kwargs):
        request = info.context.get('request')
        if request is None:
            raise GraphQLError('No se pudo obtener la solicitud.')

        # Imprimir el contexto para depuración
        print("Contexto de la solicitud:", info.context)

        cookies = request.COOKIES
        access_token = cookies.get('access_token')
        if not access_token:
            raise GraphQLError('Debes iniciar sesión')

        try:
            access_token_obj = AccessToken(access_token)
        except TokenError:
            raise GraphQLError('Token inválido')

        return func(self, info, *args, **kwargs)
    return wrapper
