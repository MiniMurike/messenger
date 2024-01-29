from django.urls import re_path

from .consumers import ChatConsumer, ChatCreateConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat-create', ChatCreateConsumer.as_asgi()),
]
