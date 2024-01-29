from django.urls import path
from django.views.generic import TemplateView

from mainMessages.views import chat


urlpatterns = [
    path('', chat),
]
