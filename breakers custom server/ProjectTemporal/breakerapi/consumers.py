# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import msgpack

#use AsyncConsumer for more complex control

#group response for 000000
class ResponseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("websocket connected.")
        await self.channel_layer.group_add("initialResponses", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("websocket disconnected.")
        pass

    async def send_response(self, event):
        print("It is active!!!!!") #debug
        await self.send(bytes_data=event)
        #await self.send(text_data=json.dumps(event["message"]))
        #if bytes_data:  # Assume x-messagepack sent as binary
            #data = msgpack.unpackb(bytes_data, raw=False)
            # Process data
            #response = {"received": data}
            #await self.send(bytes_data=msgpack.packb(response))