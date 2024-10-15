from __future__ import absolute_import, unicode_literals

# This ensures that Celery is imported when Django starts so that shared tasks work.
from .celery import app as celery_app

__all__ = ('celery_app',)
