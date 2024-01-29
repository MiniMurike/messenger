from django.urls import re_path

from .consumers import ChatConsumer, MessageConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/messages/(?P<chat_id>\w+)/$', MessageConsumer.as_asgi()),
]
