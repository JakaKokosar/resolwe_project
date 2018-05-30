"""Routing configuration for Django Channels."""
from channels.routing import route_class

from resolwe.flow.managers.consumer import ManagerConsumer
from rest_framework_reactive.routing import default_channel_routing as observers_channel_routing


channel_routing = [  # pylint: disable=invalid-name
    route_class(ManagerConsumer),
]

# Add Django Rest Framework Reactive channels routing.
channel_routing += observers_channel_routing
