"""Wait until the database accepts connections.

Runs first in the pre-deploy step (render.yaml). On a new Blueprint, the web
service's first deploy can reach this step while the new database is still
starting, and migrate would fail with "Connection refused".
"""

import time

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Wait until the database accepts connections."

    def add_arguments(self, parser):
        parser.add_argument("--timeout", type=int, default=300, help="Seconds to wait.")

    def handle(self, *args, timeout, **options):
        deadline = time.monotonic() + timeout
        while True:
            try:
                connection.ensure_connection()
                return
            except OperationalError as exc:
                if time.monotonic() >= deadline:
                    raise CommandError(
                        f"Database still unavailable after {timeout}s."
                    ) from exc
                self.stdout.write("Database not ready yet; retrying in 5s.")
                connection.close()
                time.sleep(5)
