from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_core import Agent
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str
    logs: list[str]

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        agent = Agent()
        # Ensure verbose is False for API to avoid excessive printing to stdout if not needed,
        # though logs are captured in the result
        result = agent.run(request.prompt, verbose=False)
        return ChatResponse(
            response=result["output"],
            logs=result["logs"]
        )
    except Exception as e:
        logger.error(f"Error during chat processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
