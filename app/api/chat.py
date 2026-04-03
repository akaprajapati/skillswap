from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.connection_manager import manager
from app.models.chat import Message

router = APIRouter()


@router.websocket("/ws/chat/{match_id}/{user_id}")
async def chat_socket(websocket: WebSocket, match_id: int, user_id: int):
    await manager.connect(match_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            message = data.get("message")
            receiver_id = data.get("receiver_id")

            # Save message to DB
            db: Session = next(get_db())

            msg = Message(
                match_id=match_id,
                sender_id=user_id,
                receiver_id=receiver_id,
                content=message
            )
            db.add(msg)
            db.commit()

            # Broadcast
            await manager.broadcast(match_id, {
                "sender_id": user_id,
                "message": message
            })

    except WebSocketDisconnect:
        manager.disconnect(match_id, websocket)