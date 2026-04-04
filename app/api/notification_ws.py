from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.notification_manager import manager

router = APIRouter()


@router.websocket("/ws/notifications/{user_id}")
async def notification_socket(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)