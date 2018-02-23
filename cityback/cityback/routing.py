"""Routing files that redirects clients to consumers.

See Channels documentation for detail.
"""

from channels.routing import ProtocolTypeRouter
# from channels.auth import AuthMiddlewareStack
from cityback.dashboard.consumers import ClientSocketConsumer


application = ProtocolTypeRouter({
    # WebSocket chat handler
    "websocket": ClientSocketConsumer,
})
