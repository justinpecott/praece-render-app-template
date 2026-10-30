import logging

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


def health(request):
    try:
        executor = MigrationExecutor(connection)
        pending = executor.migration_plan(executor.loader.graph.leaf_nodes())
    except Exception:
        logger.exception("Health check: database unavailable")
        return JsonResponse({"status": "error", "db": "unavailable"}, status=503)
    if pending:
        logger.error("Health check: %d unapplied migrations", len(pending))
        return JsonResponse(
            {"status": "error", "pending_migrations": len(pending)}, status=503
        )
    return JsonResponse({"status": "ok"})


@login_required
def home(request):
    return render(request, "home.html")
