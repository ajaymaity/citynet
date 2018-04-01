"""Routing files that redirects clients to consumers.

See Channels documentation for detail.
"""

from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
from django.urls import path

from cityback.rtdemo.consumers import ClientSocketConsumer
from cityback.client_interface.consumers import RTStationsConsumer

application = ProtocolTypeRouter({
    # WebSocket chat handler
    "websocket": URLRouter([
        path('ws/', ClientSocketConsumer),
        path('ws/rtStations', RTStationsConsumer),
    ]),
})
