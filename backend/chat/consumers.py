import asyncio
import json
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.db import database_sync_to_async
from users.models import User

from chat.models import Thread, Message


class ChatConsumer(AsyncConsumer):
    MAX_ACTIVE_TASKS = 40

    async def websocket_connect(self, event):
        print("entering=================")
        self.sender_user_id = int(self.scope['url_route']['kwargs']['sender_id'])
        self.receiver_user_id = int(self.scope['url_route']['kwargs']['receiver_id'])
        
        self.thread = await self.get_thread(self.sender_user_id, self.receiver_user_id)
        self.room_id = str(self.thread.id)
        self.thread_channel = f"Thread_{self.thread.id}"
        await self.channel_layer.group_add(
            self.thread_channel+str(self.sender_user_id), 
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

        print("received============ ")


    async def websocket_receive(self, event): # websocket.receive
        data =  json.loads(event["text"])
        message_data ={"message" : (data['content'])}
        self.sender_user_id = int(self.scope['url_route']['kwargs']['sender_id'])
        self.receiver_user_id = int(self.scope['url_route']['kwargs']['receiver_id'])
        message_data["sender"] = self.sender_user_id
        await self.create_chat_message(self.sender_user_id, message_data['message'])
        final_message_data = json.dumps(message_data)
        await self.channel_layer.group_send(
            self.thread_channel+str(self.receiver_user_id),
            {
                'type': 'chat_message',
                'message': final_message_data
            }
        )

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.thread_channel+str(self.sender_user_id), 
            self.channel_name
        )

    @database_sync_to_async
    def get_name(self):
        return User.objects.all()[0].username

    @database_sync_to_async
    def get_thread(self, s_user_id, r_user_id):
        try:
            return Thread.objects.get(landlord__id=s_user_id, tenant__id=r_user_id)
        except Thread.DoesNotExist:
            pass
        try:
            return Thread.objects.get(tenant__id=s_user_id,landlord__id=r_user_id)
        except Thread.DoesNotExist:
            pass
        return Thread.objects.create(tenant=User.objects.get(id=s_user_id), landlord=User.objects.get(id=r_user_id))


    @database_sync_to_async
    def create_chat_message(self, sender_id, message):
        thread = self.thread
        return Message.objects.create(thread=thread, sender=User.objects.get(id=sender_id), content=message)
