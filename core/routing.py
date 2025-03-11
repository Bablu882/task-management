from django.urls import path
from core.consumer import Consumer

ws_urlpatterns = [
    path('ws/', Consumer.as_asgi())
]