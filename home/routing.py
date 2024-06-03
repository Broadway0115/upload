from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('userpattern_update', consumers.ChatConsumer.as_asgi())
]
