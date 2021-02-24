from .base import *

DEBUG = False

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user_post"] = "100/minute"
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user_get"] = "100/minute"
