from fastapi import FastAPI, HTTPException, Depends, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from agent_core import Agent
import logging
from typing import Optional, List
from google.genai import types

# Database imports
from database import engine, Base, get_db
import models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str
    logs: list[str]
    conversation_id: int

class ConversationResponse(BaseModel):
    id: int
    created_at: str
    message_count: int

@app.post("/chat", response_model=ChatResponse)
@app.post("/chat/{conversation_id}", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    conversation_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        # 1. Handle Conversation ID
        if conversation_id:
            conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = models.Conversation()
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            conversation_id = conversation.id

        # 2. Fetch History
        history_msgs = db.query(models.Message).filter(models.Message.conversation_id == conversation_id).order_by(models.Message.id).all()

        # Convert DB messages to Gemini types
        gemini_history = []
        for msg in history_msgs:
            role = msg.role
            # Gemini expects 'user' or 'model'
            gemini_history.append(types.Content(role=role, parts=[types.Part(text=msg.content)]))

        # 3. Run Agent
        agent = Agent()
        result = agent.run(request.prompt, history=gemini_history, verbose=False)

        # 4. Save New Messages to DB
        # Save user prompt
        user_msg = models.Message(
            conversation_id=conversation_id,
            role="user",
            content=request.prompt
        )
        db.add(user_msg)

        # Save model response
        model_msg = models.Message(
            conversation_id=conversation_id,
            role="model",
            content=result["output"]
        )
        db.add(model_msg)
        db.commit()

        return ChatResponse(
            response=result["output"],
            logs=result["logs"],
            conversation_id=conversation_id
        )
    except Exception as e:
        logger.error(f"Error during chat processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
