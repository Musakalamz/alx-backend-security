from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from .models import BlockedIP, RequestLog


class IPTrackingMiddleware(MiddlewareMixin):
    geo_cache_prefix = "ip_geo:"
    geo_cache_timeout = 60 * 60 * 24

    def process_request(self, request):
        ip_address = self._get_client_ip(request)
        request.ip_address = ip_address
        geo = self._get_geolocation(ip_address) if ip_address else {}
        country = geo.get("country") or ""
        city = geo.get("city") or ""
        RequestLog.objects.create(
            ip_address=ip_address or "",
            path=request.path,
            country=country,
            city=city,
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

    def _get_geolocation(self, ip_address):
        cache_key = f"{self.geo_cache_prefix}{ip_address}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        if ip_address in {"127.0.0.1", "::1"}:
            data = {"country": "Local", "city": "Localhost"}
        else:
            data = {}
        cache.set(cache_key, data, self.geo_cache_timeout)
        return data

