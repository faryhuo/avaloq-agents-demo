from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import random

class ChatMessage(BaseModel):
    role: str
    content: str

class AvaloqAgentContext(BaseModel):
    user_name: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    messages: Optional[List[ChatMessage]] = None  # OpenAI message history
    metadata: Optional[Dict[str, Any]] = None        # 额外元数据
    extra: Optional[Dict[str, Any]] = None           # 其他扩展字段

def create_initial_context() -> AvaloqAgentContext:
    ctx = AvaloqAgentContext()
    ctx.session_id = str(random.randint(100000, 999999))
    return ctx 