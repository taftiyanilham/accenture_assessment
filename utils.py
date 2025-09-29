# auth_utils.py
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param


async def get_token_from_header_or_cookie(request: Request):
    """
    Ambil token dari Authorization header kalau ada,
    kalau tidak ada, fallback ke HttpOnly cookie.
    """
    auth = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(auth)
    if scheme.lower() == "bearer":
        return param

    token = request.cookies.get("access_token")
    return token


def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    return token
