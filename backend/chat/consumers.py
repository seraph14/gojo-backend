import asyncio
import json
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.db import database_sync_to_async
from users.models import User

from chat.models import Thread, Message


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("entering=================")
        self.sender_user_id = int(self.scope['url_route']['kwargs']['sender_id'])
        self.receiver_user_id = int(self.scope['url_route']['kwargs']['receiver_id'])
        
        self.thread = await self.get_thread(self.sender_user_id, self.receiver_user_id)
        self.room_id = str(self.thread.id)

        await self.channel_layer.group_add(
            self.room_id, 
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

        print("received============")


    async def websocket_receive(self, event): # websocket.receive
        # message_data = json.loads(event['message'])
        # message_data = ({'message' : "testing message"})
        # self.sender_user_id = int(self.scope['url_route']['kwargs']['sender_id'])
        # self.receiver_user_id = int(self.scope['url_route']['kwargs']['receiver_id'])
       

        # message_data["sender"] = self.sender_user_id
        # await self.create_chat_message(self.sender_user_id, message_data['msg'])
        # final_message_data = json.dumps(message_data)
        # await self.channel_layer.group_send(
        #     self.room_id,
        #     {
        #         'type': 'chat_message',
        #         'message': final_message_data
        #     }
        # )
        pass

    async def broadcast_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({'msg': "Loading data please wait...", 'user': 'admin'})
        })
        await asyncio.sleep(15) ### chatbot? API -> another service --> response --> send
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room_id, 
            self.channel_name
        )

    @database_sync_to_async
    def get_name(self):
        return User.objects.all()[0].username

    @database_sync_to_async
    def get_thread(self, s_user_id, r_user_id):
        try:
            return Thread.objects.get(user_1 = s_user_id, user_2=r_user_id)
        except Thread.DoesNotExist:
            pass
        try:
            return Thread.objects.get(user_2=s_user_id,user_1=r_user_id)
        except Thread.DoesNotExist:
            pass
        return Thread.objects.create(user_1=User.objects.get(id=s_user_id), user_2=User.objects.get(id=r_user_id))


    @database_sync_to_async
    def create_chat_message(self, sender_id, message):
        thread = self.thread
        return Message.objects.create(thread=thread, sender=User.objects.get(id=sender_id), content=message)
