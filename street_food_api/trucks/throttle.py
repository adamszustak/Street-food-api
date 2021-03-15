from rest_framework import throttling

from .middlewares import AddHeaders


class ThrottleHeaders:
    def throttle_success(self):
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
        # print(self.key, self.history, self.duration)
        # print(f"REMAIN TIME {self.duration - (self.now - self.history[-1])}")
        # print(f"LIMIT {self.get_rate()}")
        # print(f"REMAIN RATE {self.num_requests - len(self.history) + 1}")
        return True

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
