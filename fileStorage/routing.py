from django.urls import re_path
from .consumers import SearchConsumer


websocket_urlpatterns = [
    re_path(r'^bill/create/(?P<pk>[\d]+)/(?P<slug>[\w-]+)/$', SearchConsumer),
]