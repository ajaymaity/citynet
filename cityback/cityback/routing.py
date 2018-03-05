"""Routing files that redirects clients to consumers.

See Channels documentation for detail.
"""

from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
from django.urls import path
from cityback.dashboard.consumers import ClientSocketConsumer
from cityback.visualisation.consumers import RTStationsConsumer

application = ProtocolTypeRouter({
    # WebSocket chat handler
    "websocket": URLRouter([
        path('ws/', ClientSocketConsumer),
        path('ws/rtStations', RTStationsConsumer),
    ]),
})
