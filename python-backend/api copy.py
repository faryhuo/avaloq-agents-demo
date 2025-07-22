from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
import asyncio
from typing import Dict, List, Optional, Any
from uuid import uuid4
from datetime import datetime
import json

from context import AvaloqAgentContext
from triage_agent import avaloq_triage_agent
from agents import Runner
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str  # 'system', 'user', 'assistant', etc.
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]
    stream: bool = False
    user_name: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None        # 额外元数据
    extra: Optional[Dict[str, Any]] = None 

class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str = "stop"

class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    created: int
    choices: List[ChatCompletionChoice]
    topic: str
    user_name: str
    user_id: str
    session_id: str
    messages: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    extra: Dict[str, Any]


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def openai_chat_completions(req: ChatCompletionRequest, request: Request):
    user_message = next(
        (
            m
            for m in reversed(req.messages)
            if (m.get("role") if isinstance(m, dict) else getattr(m, "role", None)) == "user"
        ),
        None,
    )
    if not user_message:
        raise HTTPException(status_code=400, detail="No user message found.")
    ctx = AvaloqAgentContext(
        user_name=req.user_name,
        user_id=req.user_id,
        session_id=req.session_id,
        messages=[m for m in req.messages],
        # 其他字段可按需补充
    )
    stream = getattr(req, 'stream', False)
    try:
        result = await Runner.run(avaloq_triage_agent, user_message.content, context=ctx)
        if hasattr(result, 'final_output'):
            response_text = result.final_output
        elif hasattr(result, 'final_output_as'):
            response_text = result.final_output_as(str)
        else:
            response_text = str(result)
        assistant_message = ChatMessage(role="assistant", content=response_text)
        if stream:
            # OpenAI SSE 格式
            async def event_generator():
                for chunk in response_text.split():
                    data = {
                        "id": f"chatcmpl-{uuid4().hex}",
                        "object": "chat.completion.chunk",
                        "created": int(datetime.now().timestamp()),
                        "choices": [
                            {"delta": {"role": "assistant", "content": chunk}, "index": 0, "finish_reason": None}
                        ],
                    }
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                # 结束信号
                yield "data: [DONE]\n\n"
            return StreamingResponse(event_generator(), media_type="text/event-stream")
        else:
            return ChatCompletionResponse(
                created=int(datetime.now().timestamp()),
                choices=[ChatCompletionChoice(index=0, message=assistant_message, finish_reason="stop")],
                topic=  "",
                user_name=req.user_name or "",
                user_id=req.user_id or "",
                session_id=req.session_id or "",
                messages=[m if isinstance(m, dict) else m.dict() for m in (req.messages or [])],
                metadata=req.metadata or {},
                extra=req.extra or {},
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 