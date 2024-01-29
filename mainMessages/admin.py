from django.contrib import admin

from mainMessages.models import UserProfile, Chat, Message, ChatUser, ChatMessages

admin.site.register(UserProfile)
admin.site.register(Chat)
admin.site.register(Message)

admin.site.register(ChatMessages)
admin.site.register(ChatUser)
