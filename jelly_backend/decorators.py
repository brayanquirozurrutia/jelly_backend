import os
import jwt
from graphql import GraphQLError
from functools import wraps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


def jwt_required(
        permission_required: callable = None
) -> callable:
    """
    Decorator to check if a JWT token is provided in the request and if it is valid.
    :param permission_required: A callable that checks if the user has the required permission.
    :return: A decorator function.
    """
    def decorator(func):
        @wraps(func)
        def wrapped(root, info, *args, **kwargs):
            request = info.context
            access_token = request.COOKIES.get('access_token')

            if not access_token:
                raise GraphQLError('No JWT token provided')

            try:
                secret_key = os.getenv('SECRET_KEY')
                payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise GraphQLError('JWT token has expired')
            except jwt.InvalidTokenError as e:
                raise GraphQLError(f'Invalid JWT token: {str(e)}')

            # Simular usuario basado en la carga útil del token
            user_id = payload.get('user_id')
            if user_id:
                User = get_user_model()
                try:
                    user = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    user = AnonymousUser()
                request.user = user
            else:
                request.user = AnonymousUser()

            if permission_required:
                permission_checker = permission_required()
                # Pasar 'None' como argumento 'view' para cumplir con la firma del método
                if not permission_checker.has_permission(request, None):
                    raise GraphQLError('Permission denied')

            return func(root, info, *args, **kwargs)

        return wrapped

    return decorator
