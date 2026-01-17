from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from .models import BlockedIP, RequestLog


class IPTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = self._get_client_ip(request)
        request.ip_address = ip_address
        RequestLog.objects.create(
            ip_address=ip_address or "",
            path=request.path,
        )
        if ip_address and BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Forbidden")

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

