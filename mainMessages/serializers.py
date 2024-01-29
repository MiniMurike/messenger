from rest_framework import serializers
from .models import Message, UserProfile, Chat, ChatMessages, ChatUser, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)


class PUserSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer

    class Meta:
        model = UserProfile
        fields = ('user', 'nickname', 'avatar',)

    def to_representation(self, instance):
        rep = super(PUserSerializer, self).to_representation(instance)
        rep['user'] = instance.user.username

        return rep


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    sender = PUserSerializer

    class Meta:
        model = Message
        fields = ('sender', 'text',)


class ChatUserSerializer(serializers.HyperlinkedModelSerializer):
    # chat = ChatSerializer
    # user = PUserSerializer

    class Meta:
        model = ChatUser
        fields = ('chat', 'user',)

    def to_representation(self, instance):
        rep = super(ChatUserSerializer, self).to_representation(instance)
        rep['user'] = instance.user.user.username
        rep['chat'] = instance.chat.title

        return rep


class ChatMessagesSerializer(serializers.HyperlinkedModelSerializer):
    # chat = ChatSerializer
    # message = MessageSerializer

    class Meta:
        model = ChatMessages
        fields = ('chat', 'message',)

    def to_representation(self, instance):
        rep = super(ChatMessagesSerializer, self).to_representation(instance)
        rep['message'] = instance.message.text
        rep['chat'] = instance.chat.title

        return rep


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    chat_messages = ChatMessagesSerializer
    chat_users = ChatUserSerializer

    class Meta:
        model = Chat
        fields = ('title', 'chat_messages', 'chat_users',)

    # def to_representation(self, instance):
    #     print(instance.chat_messages)
    #     rep = super(ChatSerializer, self).to_representation(instance)
    #     rep['title'] = instance.title
    #
    #     return rep


