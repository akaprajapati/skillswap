from fastapi import WebSocket


class NotificationManager:
    def __init__(self):
        self.connections = {}  # user_id -> websocket

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.connections:
            del self.connections[user_id]

    async def send(self, user_id: int, data: dict):
        if user_id in self.connections:
            await self.connections[user_id].send_json(data)


manager = NotificationManager()