"""Middleware file helps to take logs."""
from time import time

from main.models import Logger


class SimpleMiddleware:
    """Simple-Middleware Class."""

    def __init__(self, get_response):
        """Simple-Middleware Init."""
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        """Simple-Middleware Call."""
        print('before')
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        st = time()
        response = self.get_response(request)
        print('after')
        print(f"Time executed:{time() - st}; path:{request.path}")
        # Code to be executed for each request/response after
        # the view is called.

        return response


def get_client_ip(request):
    """Client IP."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class LogMiddleware:
    """Log-Middleware Class."""

    def __init__(self, get_response):
        """Log-Middleware Class init."""
        self.get_response = get_response

    def __call__(self, request):
        """Log-Middleware call."""
        logger = Logger()
        logger.save()
        response = self.get_response(request)

        if request.method == "GET":
            print("lets go!")
            st = time()
            path = request.get_full_path()
            user_ip = get_client_ip(request)
            utm = request.GET.get("utm")
            time_ex = time() - st
            logger = Logger(utm=str(utm), time_execution=time_ex, user_ip=user_ip, path=path)
            logger.save()

        return response
