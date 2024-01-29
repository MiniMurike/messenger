import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Chat, Message, UserProfile, ChatMessages, ChatUser


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = None
        self.room = None

    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room = Chat.objects.get(id=self.chat_id)

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.chat_id,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_id,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'send_message':
            self._send_message(text_data_json)
        elif type == 'get_users':
            self._get_users(text_data_json)
        elif type == 'add_user':
            user = None

            try:
                user = get_object_or_404(User, id=text_data_json['user_id'])
            except Exception as e:
                return
            # user = User.objects.get(id=text_data_json['user_id'])
            p_user = UserProfile.objects.get(user=user)

            try:
                ChatUser.objects.get(
                    chat=text_data_json['chat_id'],
                    user=p_user,
                )
            except Exception:
                ChatUser.objects.create(
                    chat=Chat.objects.get(
                        id=text_data_json['chat_id']),
                    user=p_user,
                )

            self._get_users(text_data_json)
        elif type == 'delete_user':
            user = None
            try:
                user = get_object_or_404(User, id=text_data_json['user_id'])
            except Exception as e:
                return
            # user = User.objects.get(id=text_data_json['user_id'])
            p_user = UserProfile.objects.get(user=user)

            try:
                ChatUser.objects.get(
                    chat=Chat.objects.get(
                        id=text_data_json['chat_id']),
                    user=p_user,
                ).delete()
            except Exception as e:
                return

            self._get_users(text_data_json)
        elif type == 'create_chat':
            user = User.objects.get(id=text_data_json['user_id'])
            p_user = UserProfile.objects.get(user=user)
            chat = Chat.objects.create(
                title=text_data_json['title'],
            )
            ChatUser.objects.create(
                chat=chat,
                user=p_user,
            )
            self.send(json.dumps({'type': 'reload'}))

    def _get_users(self, data):
        chat_users = ChatUser.objects.filter(chat__id=data['chat_id'])
        response = []
        for item in chat_users:
            response.append({
                'nickname': item.user.nickname,
                'avatar': item.user.avatar.url,
            })
        async_to_sync(self.channel_layer.group_send)(
            self.chat_id, {
                'type': 'get_users',
                'data': response,
            }
        )

    def _send_message(self, data):
        message = data['message']
        user_id = data['user_id']
        user = User.objects.get(id=user_id)
        profile_user = UserProfile.objects.get(user=user)

        msg = Message.objects.create(
            sender=UserProfile.objects.get(
                user=User.objects.get(
                    id=user_id)),
            text=message
        )
        ChatMessages.objects.create(
            chat=Chat.objects.get(id=self.chat_id),
            message=msg,
        )

        async_to_sync(self.channel_layer.group_send)(
            self.chat_id, {
                'type': 'message_send',
                'message': message,
                'user_nickname': profile_user.nickname,
                'user_id': user_id,
                'avatar': profile_user.avatar.url,
            }
        )

    def message_send(self, event):
        self.send(text_data=json.dumps(event))

    def get_users(self, event):
        self.send(text_data=json.dumps(event))


class MessageConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = None

    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        chat_id = text_data_json['chat_id']

        chat = Chat.objects.get(id=chat_id).chat_messages.all()
        response = [{'type': 'get_messages'}]
        for value in chat:
            response.append({
                'user_nickname': value.sender.nickname,
                'user_id': value.sender.user.id,
                'message': value.text,
                'avatar': value.sender.avatar.url,
            })

        self.send(json.dumps(response))
