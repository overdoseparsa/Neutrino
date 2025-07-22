# path: yourapp/middleware/xss_middleware.py

from django.http import JsonResponse
from neutrino.core.provider import XssSecurityProvider

class XssSanitizerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['POST', 'PUT']:
            try:
                XssSecurityProvider(request)
            except Exception as e:
                return JsonResponse(
                    {'error': 'Potential XSS attack detected', 'detail': str(e)},
                    status=403
                )
        return self.get_response(request)
