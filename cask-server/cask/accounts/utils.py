import logging
from hashlib import sha1
from typing import Optional

from django.conf import settings
from django.contrib.auth.models import User
from itsdangerous import BadSignature, TimedJSONWebSignatureSerializer

logger = logging.getLogger("cask")


def generate_token(user: User, expires_in: int = 3600 * 24 * 30) -> str:
    s = TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY, expires_in=expires_in, salt="auth"
    )
    payload = {"uid": str(user.id), "sh": security_hash(user)}
    return s.dumps(payload).decode("utf-8")


def parse_token(token: str) -> Optional[str]:
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, salt="auth")
    try:
        payload = s.loads(token)
    except BadSignature:
        logger.warning("auth: bad signature")
        return None
    if "uid" not in payload:
        logger.warning("auth: missing uid")
        return None
    if "sh" not in payload:
        logger.warning("auth: missing security hash")
        return None
    return payload


def security_hash(user: User) -> str:
    return sha1(user.password.encode("utf-8")).hexdigest()
