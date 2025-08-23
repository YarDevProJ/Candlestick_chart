from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/candles/(?P<symbol>\w+)/(?P<interval>\w+)/$', consumers.CandleConsumer.as_asgi()),
]