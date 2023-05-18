from channels.generic.websocket import WebsocketConsumer
import json



'''
=> all Chat
chat/

chat/thread_id/

chat/thread_id/:receiver { message: data }

'''

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        recipient = text_data_json['recipient']

        # Send message to recipient
        self.channel_layer.group_send(
            f'chat_{recipient}',
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'recipient': recipient
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        recipient = event['recipient']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recipient': recipient
        }))