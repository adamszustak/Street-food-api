from .base import *

DEBUG = False

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

AUTH_USER_MODEL = "users.User"
