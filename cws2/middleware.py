from django.utils import timezone


class LogUserLastSeenMiddleware:
    def get_ip_address(self, request):
        return request.META.get("HTTP_X_FORWARDED_FOR", None) or request.META.get(
            "REMOTE_ADDR"
        )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(request, "user") and request.user.is_authenticated:
            request.user.last_seen_ip = self.get_ip_address(request)
            request.user.last_seen_route = request.resolver_match.url_name[:64]
            request.user.last_seen_at = timezone.now()
            request.user.save(
                update_fields=["last_seen_ip", "last_seen_route", "last_seen_at"]
            )
        return response
