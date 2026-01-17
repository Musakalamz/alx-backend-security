from django.core.management.base import BaseCommand

from ip_tracking.models import BlockedIP


class Command(BaseCommand):
    help = "Add an IP address to the blocked list."

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str)

    def handle(self, *args, **options):
        ip_address = options["ip_address"].strip()
        if not ip_address:
            self.stderr.write("Invalid IP address.")
            return
        obj, created = BlockedIP.objects.get_or_create(ip_address=ip_address)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Blocked IP {ip_address}"))
        else:
            self.stdout.write(f"IP {ip_address} is already blocked")

