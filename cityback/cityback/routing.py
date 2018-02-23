from cityback.dashboard import consumers

from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from cityback.dashboard.consumers import ClientSocketConsumer


application = ProtocolTypeRouter({
    # WebSocket chat handler
    "websocket": ClientSocketConsumer,
})

