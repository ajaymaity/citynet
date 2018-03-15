from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser(username='admin',
                                      password='admin',
                                      email='your@email.PK')
        print("admin/admin account created!")
