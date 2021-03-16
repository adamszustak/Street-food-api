import math


class AddHeaders:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            klass = AddHeaders.th
        except AttributeError:
            pass
        else:
            limit = klass.get_rate()
            remaining = klass.num_requests - len(klass.history)
            reset = math.floor(
                (klass.duration - (klass.now - klass.history[-1])) / 60
            )
            if request.method == "GET":
                response["X-RATE-LIMIT-LIMIT-GET"] = limit
                response["X-RATE-LIMIT-REMAINING-GET"] = remaining
                response["X-RATE-LIMIT-RESET-GET"] = reset
            elif request.method in ("POST", "PUT", "PATCH"):
                response["X-RATE-LIMIT-LIMIT-POST"] = limit
                response["X-RATE-LIMIT-REMAINING-POST"] = remaining
                response["X-RATE-LIMIT-RESET-POST"] = reset
        finally:
            return response

    @classmethod
    def get_throttle(cls, th):
        cls.th = th
