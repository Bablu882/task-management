from channels.generic.websocket import AsyncJsonWebsocketConsumer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from asgiref.sync import sync_to_async
from task.models.user import User
from channels.exceptions import DenyConnection


def get_group_name(agent: User):
    return f"{agent.id}"


class Consumer(AsyncJsonWebsocketConsumer):

    async def get_user(self, token):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = await sync_to_async(jwt_auth.get_validated_token)(token)
            user = await sync_to_async(jwt_auth.get_user)(validated_token)
        except (AuthenticationFailed, InvalidToken) as e:
            raise DenyConnection(e)
        else:
            return user

    async def connect(self):
        token = self.scope['query_string'].decode().split('=')[1]
        self.user = await self.get_user(token)
        self.chatroom_id = get_group_name(self.user)
        await self.channel_layer.group_add(self.chatroom_id, self.channel_name)
        await self.channel_layer.group_add('broadcast', self.channel_name)
        await self.accept()


    async def outgoing(self, event):
        """
        Sends data to agents. Could be a whatsapp msg from user or agents own message that he/she sent.
        event: {type: funcName, data:{msg: '', mes_type: '', code: defined in docs}}
        """
        await self.send_json(event['data'])

    # async def receive_json(self, content, **kwargs):
    #     pass

    # async def disconnect(self, code):
    #     pass
        # await self.channel_layer.group_discard(
        #     get_group_name(self.user),
        #     self.channel_name
        # )
        # await self.channel_layer.group_discard(
        #     self.company_chatroom_id,
        #     self.channel_name
        # )
