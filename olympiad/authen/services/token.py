from datetime import timedelta, datetime

import jwt
from django.conf import settings


def JWTToken(user_id: int) -> dict:
    """Обоработка данных для создания токена"""

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'user_id': user_id,
        'access_token': NewAccessToken(data={'user_id': user_id}, time_exp=access_token_expires),
        'token_type': 'Token'
    }


def NewAccessToken(data: dict, time_exp: timedelta = None):
    """Создание JWT токена"""
    reserv = data.copy()

    if timedelta is not None:
        expire = datetime.now() + time_exp
    else:
        expire = datetime.now() + timedelta(minutes=15)

    reserv.update({'exp': expire, 'sub': 'access'})
    jwt_token = jwt.encode(reserv, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_token
