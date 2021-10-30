import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .views import *

from .models import Chat,Message,Contact
from django.utils.html import strip_tags
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.room_name
      #  print(self.room_name)
      #  print(self.room_group_name)
      #  print(self.channel_name)
        # Join room group
        async_to_sync( self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        #print(self.channel_layer)
        self.accept()
#        print(len(Group(self.room_group_name).channel_layer.group_channels(self.channel_name)))
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        userid = text_data_json['userid']
        chatid = text_data_json['chatid']
        #socketuser = event['userid']
        user= User.objects.get(id=userid)
        messagebody = strip_tags(message)
        
       # print(user)
       # print(chat_id)

        message_new = Message(
            author=user,
            content=messagebody)
        message_new.save()
        
        current_chat = get_current_chat(chatid)
        current_chat.messages.add(message_new)
        current_chat.save()
        dt = message_new.timestamp
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'userid': user.username,
                'chatid': chatid,
                'timestamp': str(dt.strftime('%H:%M:%S')),
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        socketuser = event['userid']
       
        messagebody = event['message']
        chat_id = event['chatid'] 
        timestamp = event['timestamp']
        
        if 'url' in event:
            url = event['url']
            self.send(text_data=json.dumps({
            'message': strip_tags(messagebody),
            'timestamp': timestamp,
            'user':socketuser,
            'url':url,

        }))
        else:
        # Send message to WebSocket
            self.send(text_data=json.dumps({
            'message': strip_tags(messagebody),
            'timestamp': timestamp,
            'user':socketuser,

        }))