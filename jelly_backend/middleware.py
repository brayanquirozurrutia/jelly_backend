from django.utils.deprecation import MiddlewareMixin


class JWTAuthCookieMiddleware(MiddlewareMixin):
    """
    Middleware to process the request and add the 'Authorization' header with the JWT token
    from the 'access_token' cookie.
    """
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        csrf_token = request.COOKIES.get('csrftoken')

        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        if csrf_token:
            request.META['HTTP_X_CSRFTOKEN'] = csrf_token
