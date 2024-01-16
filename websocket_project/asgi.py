"""
ASGI config for websocket_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from home.routing import websocket_urlpatterns
from app_2.routing import app_websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websocket_project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns + app_websocket_urlpatterns)
        ),
    }
)
