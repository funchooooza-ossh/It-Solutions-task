from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import datetime
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.http import JsonResponse


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):

        token_from_cookies = request.COOKIES.get("access_token", "")
        token_from_header = request.META.get("HTTP_JWT", "")

        if token_from_cookies:
            request.META["HTTP_JWT"] = f"JWT {token_from_cookies}"
        elif token_from_header:
            request.META["HTTP_JWT"] = token_from_header

        if not token_from_cookies and not token_from_header:
            return None


class RefreshTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if access_token:
            try:
                access_token_obj = AccessToken(access_token)

                if access_token_obj.get("exp") < datetime.datetime.now().timestamp():
                    raise TokenError("Token is expired")

            except TokenError:

                if refresh_token:
                    try:
                        refresh_token_obj = RefreshToken(refresh_token)
                        new_access_token = str(refresh_token_obj.access_token)

                        response = redirect(request.path)
                        response.set_cookie(
                            "access_token", new_access_token, httponly=True
                        )

                        response["X-Token-Refreshed"] = "true"
                        return response
                    except TokenError:

                        return JsonResponse(
                            {
                                "error": "Refresh token is invalid or expired. Please log in again."
                            },
                            status=401,
                        )
                else:
                    rs = HttpResponseRedirect(request.build_absolute_uri('/login/'))
                    rs.delete_cookie('access_token')
                    return rs

        # Если токены действительны, просто продолжаем обработку запроса
        response = self.get_response(request)
        return response
