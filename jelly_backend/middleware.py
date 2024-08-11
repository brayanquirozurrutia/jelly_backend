from django.utils.deprecation import MiddlewareMixin
from django_ratelimit.core import get_usage
from django.http import HttpResponse


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

# TODO: DEJAR EL RATE LIMIT POR ENDPOINT NO GLOBAL


class GlobalRateLimitMiddleware(MiddlewareMixin):
    """
    Middleware to apply a global rate limit of 5 requests per minute.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        is_ratelimited = get_usage(request, fn=view_func, key='ip', rate='20/m', method=['POST'], increment=True)
        if is_ratelimited['should_limit']:
            return HttpResponse('Too Many Requests', status=429)