import os
import sys
import uuid
from fastapi import APIRouter, HTTPException

# Ensure coderAgent directory is in sys.path so its child imports resolve correctly
coder_agent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "agent", "coderAgent"))
if coder_agent_dir not in sys.path:
    sys.path.insert(0, coder_agent_dir)

from orchestrator import run_pipeline
from app.agent.collab_code import shopbot_respond
from app.schemas.chat import ChatRequest, ChatResponse, PipelineRequest
from app.schemas.response import ApiResponse

router = APIRouter()


@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    REST API endpoint that receives a JSON payload, processes it via the ChatController,
    and returns the chatbot's response.
    """
    try:
        response, thread_id = get_response(request.message, request.thread_id)
        return ApiResponse(data=ChatResponse(response=response, thread_id=thread_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run-coder")
def run_pipeline_endpoint(request: PipelineRequest):
    """
    REST API endpoint that receives a JSON payload, triggers the multi-agent code generation pipeline,
    and returns the result (code, tests, status, and history).
    """
    try:
        result = run_pipeline(request.request, request.max_iterations)
        return ApiResponse(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_response(message: str, thread_id: str = None) -> tuple:
    """
    Invokes the chatbot response logic from collab_code.py.
    
    Args:
        message: The customer query string.
        thread_id: The conversation thread ID for session memory.
        
    Returns:
        A tuple of (response_text, active_thread_id).
    """
    if not thread_id:
        thread_id = f"session-{uuid.uuid4().hex[:8]}"
    
    # Prepare session state dict required by shopbot_respond
    session_state = {"thread_id": thread_id}
    
    # Call the chatbot logic with an empty history list (memory is managed via thread_id)
    response = shopbot_respond(message, [], session_state)
    return response, thread_id

