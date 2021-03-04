from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = ["*"]

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
]

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user_post"] = "2/minute"
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user_get"] = "10/minute"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "cache",
    }
}

##### TO IMPLEMENT #####

# SECURE_REFERRER_POLICY = 'same-origin'
# X_FRAME_OPTIONS = 'DENY'
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS = 31536000
