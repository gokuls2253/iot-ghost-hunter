import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 1. Join the "dashboard_feed" group
        self.group_name = "dashboard_feed"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket Connected: {self.channel_name}")

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from the group (Broadcast)
    async def device_update(self, event):
        message = event['message']

        # Send message to WebSocket (The Browser)
        await self.send(text_data=json.dumps({
            'message': message
        }))