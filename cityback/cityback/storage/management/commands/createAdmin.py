"""Create a dev admin account."""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Custom command."""

    def handle(self, *args, **options):
        """Actual code."""
        User.objects.create_superuser(username='admin',
                                      password='admin',
                                      email='your@email.PK')
        print("admin/admin account created!")
