"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import sys
sys.path.append('../')
import home.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    'http': django_asgi_app,

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter(
            home.routing.websocket_urlpatterns
        )
    ),
})

# application = get_asgi_application()
