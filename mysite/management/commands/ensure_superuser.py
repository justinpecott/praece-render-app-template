"""Create the first superuser from environment variables, once.

Runs on every deploy (render.yaml preDeployCommand). Does nothing if
DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD is unset or a superuser
already exists, so it never changes or overwrites an existing account.
DJANGO_SUPERUSER_EMAIL is optional.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser from DJANGO_SUPERUSER_* variables if none exists."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        if not (username and password):
            return

        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(f"Created superuser {username!r}.")
