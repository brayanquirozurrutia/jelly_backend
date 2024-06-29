from functools import wraps
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from graphql import GraphQLError


def validate_token(func):
    @wraps(func)
    def wrapper(self, info, *args, **kwargs):
        authorization_header = info.context.headers.get('Authorization')
        if not authorization_header or not authorization_header.startswith('Bearer '):
            raise GraphQLError('Debes iniciar sesión')

        token = authorization_header.split()[1]
        try:
            access_token = AccessToken(token)
            if not access_token:
                raise GraphQLError('Token inválido')
        except TokenError:
            raise GraphQLError('Token inválido')

        return func(self, info, *args, **kwargs)
    return wrapper
