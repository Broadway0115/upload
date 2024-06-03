from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

channelList = []


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        channelList.append(self)
        async_to_sync(self.channel_layer.group_add)(
            'test',
            channel=self.channel_name
        )
        self.accept()
