from django.http import HttpResponse
from django_ratelimit.core import is_ratelimited


def login_view(request):
    if request.method != "POST":
        return HttpResponse("Login page", status=200)
    if request.user.is_authenticated:
        limited = is_ratelimited(
            request,
            group="login_auth",
            key="user",
            rate="10/m",
            method=["POST"],
            increment=True,
        )
    else:
        limited = is_ratelimited(
            request,
            group="login_anon",
            key="ip",
            rate="5/m",
            method=["POST"],
            increment=True,
        )
    if limited:
        return HttpResponse("Too many requests", status=429)
    return HttpResponse("Login successful", status=200)
