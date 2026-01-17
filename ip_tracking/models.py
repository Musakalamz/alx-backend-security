from django.db import models


class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=2048)


class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)
