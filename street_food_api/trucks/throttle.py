from rest_framework import throttling

from .middlewares import AddHeaders


class ThrottleHeaders:
    def allow_request(self, request, view):
        AddHeaders.get_throttle(self)
        return super().allow_request(request, view)


class UserPostRateThrottle(ThrottleHeaders, throttling.UserRateThrottle):
    scope = "user_post"

    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)


class UserGetRateThrottle(ThrottleHeaders, throttling.UserRateThrottle):
    scope = "user_get"

    def allow_request(self, request, view):
        if request.method in ("POST", "PUT", "PATCH"):
            return True
        return super().allow_request(request, view)
