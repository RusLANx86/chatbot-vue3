from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import random
import asyncio
import json
from datetime import datetime
import aiohttp
import os

from database import get_db, init_db
from models import Message, MessageCreate, MessageResponse
from bot import ChatBot

app = FastAPI(title="Vue3 Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_bot = ChatBot()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Удаляем неактивные соединения
                self.active_connections.remove(connection)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    """Инициализация базы данных при запуске"""
    await init_db()

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "Vue3 Chat API", "version": "1.0.0"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "new_message":
                db = next(get_db())
                db_message = Message(
                    sender=message_data["sender"],
                    text=message_data["text"],
                    timestamp=datetime.utcnow()
                )
                db.add(db_message)
                db.commit()
                db.refresh(db_message)
                
                await manager.broadcast(json.dumps({
                    "type": "new_message",
                    "message": {
                        "id": db_message.id,
                        "sender": db_message.sender,
                        "text": db_message.text,
                        "timestamp": db_message.timestamp.isoformat()
                    }
                }))
                
                if message_data["sender"] != "Bot":
                    asyncio.create_task(send_bot_response_ws(db, message_data["text"]))
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def send_bot_response_ws(db: Session, user_message: str):
    """Асинхронно отправляет ответ бота через WebSocket"""
    await asyncio.sleep(random.uniform(1, 3))  # Задержка 1-3 секунды
    
    bot_response = await chat_bot.get_response(user_message)
    
    db_message = Message(
        sender="Bot",
        text=bot_response,
        timestamp=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Отправляем ответ бота всем подключенным клиентам
    await manager.broadcast(json.dumps({
        "type": "new_message",
        "message": {
            "id": db_message.id,
            "sender": db_message.sender,
            "text": db_message.text,
            "timestamp": db_message.timestamp.isoformat()
        }
    }))

@app.get("/messages", response_model=List[MessageResponse])
async def get_messages(db: Session = Depends(get_db)):
    """Получить все сообщения"""
    messages = db.query(Message).order_by(Message.timestamp).all()
    return messages

@app.post("/messages", response_model=MessageResponse)
async def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """Создать новое сообщение"""
    db_message = Message(
        sender=message.sender,
        text=message.text,
        timestamp=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Отправляем сообщение всем подключенным WebSocket клиентам
    await manager.broadcast(json.dumps({
        "type": "new_message",
        "message": {
            "id": db_message.id,
            "sender": db_message.sender,
            "text": db_message.text,
            "timestamp": db_message.timestamp.isoformat()
        }
    }))
    
    # Если сообщение не от бота, генерируем ответ бота
    if message.sender != "Bot":
        asyncio.create_task(send_bot_response(db, message.text))
    
    return db_message

@app.post("/bot/respond")
async def bot_respond(message: MessageCreate, db: Session = Depends(get_db)):
    """Получить ответ от бота"""
    bot_response = await chat_bot.get_response(message.text)
    
    db_message = Message(
        sender="Bot",
        text=bot_response,
        timestamp=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return db_message

async def send_bot_response(db: Session, user_message: str):
    """Асинхронно отправляет ответ бота"""
    await asyncio.sleep(random.uniform(1, 3))  # Задержка 1-3 секунды
    
    bot_response = await chat_bot.get_response(user_message)
    
    db_message = Message(
        sender="Bot",
        text=bot_response,
        timestamp=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Отправляем ответ бота всем подключенным WebSocket клиентам
    await manager.broadcast(json.dumps({
        "type": "new_message",
        "message": {
            "id": db_message.id,
            "sender": db_message.sender,
            "text": db_message.text,
            "timestamp": db_message.timestamp.isoformat()
        }
    }))

@app.delete("/messages")
async def clear_messages(db: Session = Depends(get_db)):
    """Очистить все сообщения"""
    db.query(Message).delete()
    db.commit()
    
    # Уведомляем всех WebSocket клиентов об очистке
    await manager.broadcast(json.dumps({
        "type": "clear_messages"
    }))
    
    return {"message": "All messages cleared"}

@app.get("/bot/status")
async def bot_status():
    """Получить статус LLM"""
    try:
        # Проверяем доступность Ollama
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{os.getenv('OLLAMA_URL', 'http://localhost:11434')}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    model_name = os.getenv('OLLAMA_MODEL', 'llama2:7b')
                    models = [model['name'] for model in data.get('models', [])]
                    
                    if model_name in models:
                        # Тестируем модель
                        test_payload = {
                            "model": model_name,
                            "prompt": "test",
                            "stream": False,
                            "options": {
                                "temperature": 0.7,
                                "max_tokens": 10
                            }
                        }
                        
                        async with session.post(
                            f"{os.getenv('OLLAMA_URL', 'http://localhost:11434')}/api/generate",
                            json=test_payload,
                            timeout=aiohttp.ClientTimeout(total=5)
                        ) as test_response:
                            if test_response.status == 200:
                                return {"status": "ready", "model": model_name}
                            else:
                                return {"status": "loading", "model": model_name}
                    else:
                        return {"status": "error", "message": f"Модель {model_name} не найдена"}
                else:
                    return {"status": "error", "message": "Ollama недоступна"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 