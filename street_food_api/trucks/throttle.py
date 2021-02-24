from rest_framework import throttling


class UserGetRateThrottle(throttling.UserRateThrottle):
    scope = "user_get"

    def allow_request(self, request, view):
        if request.method == "POST":
            return True
        return super().allow_request(request, view)


class UserPostRateThrottle(throttling.UserRateThrottle):
    scope = "user_post"

    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)
