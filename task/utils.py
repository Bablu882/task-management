from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, date
from rest_framework.pagination import PageNumberPagination
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):

        if isinstance(value, date) and not isinstance(value, datetime):
            return value.strftime("%d %B %Y")
        
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        value = timezone.localtime(value)
        return value.strftime("%d %B %Y, %I:%M %p")
    

class SearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 120


def websocket_trigger(group, type_, data):
    channel_layer = get_channel_layer()
    group_name = group
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': type_,
            'data': data
        }
    )


def send_socket_notification(user_ids, code, message):
    for user_id in user_ids:
        group_name = f"{user_id}"
        data = {
            'code': code,
            'body': message,
        }
        websocket_trigger(group_name, 'outgoing', data)