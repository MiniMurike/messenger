from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets

from mainMessages.models import UserProfile, Chat, Message, ChatUser, ChatMessages
from mainMessages.serializers import ChatMessages, MessageSerializer, PUserSerializer, UserSerializer, ChatSerializer, \
    ChatMessagesSerializer, ChatUserSerializer


@login_required
def chat(request):
    user = UserProfile.objects.get(user=request.user)
    chat_list = Chat.objects.filter(chat_users=user)

    return render(request, 'chat.html', {'chat_list': chat_list},)


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class PUserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = PUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChatMessagesViewSet(viewsets.ModelViewSet):
    queryset = ChatMessages.objects.all()
    serializer_class = ChatMessagesSerializer


class ChatUsersViewSet(viewsets.ModelViewSet):
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer
