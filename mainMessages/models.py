from django.contrib.auth.models import User
from django.db import models


def upload_path(instance, filename):
    return f'user_{instance.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=64)
    avatar = models.ImageField(
        default='default_avatar.png',
        upload_to=upload_path,
    )

    def __str__(self):
        return self.nickname


class Chat(models.Model):
    title = models.CharField(
        max_length=128,
    )
    chat_messages = models.ManyToManyField(
        to='Message',
        through='ChatMessages',
    )
    chat_users = models.ManyToManyField(
        to=UserProfile,
        through='ChatUser',
    )

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
    )
    text = models.TextField()

    def __str__(self):
        return self.text


class ChatMessages(models.Model):
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
    )
    message = models.ForeignKey(
        to=Message,
        on_delete=models.CASCADE,
    )


class ChatUser(models.Model):
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
    )
