import asyncio
import uuid
from typing import Any, Dict, Optional


class ContextManager:
    """管理任务的上下文信息，允许不同 Agent 共享数据"""

    def __init__(self):
        self.contexts: Dict[str, Dict[str, Any]] = {}  # 任务 ID -> 上下文数据
        self.lock = asyncio.Lock()  # 保护并发访问上下文数据

    async def create_context(self) -> str:
        """创建一个新的上下文"""
        context_id = str(uuid.uuid4())
        async with self.lock:
            self.contexts[context_id] = {}
        return context_id

    async def get_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """获取上下文数据"""
        async with self.lock:
            return self.contexts.get(context_id, {}).copy()

    async def update_context(self, context_id: str, data: Dict[str, Any]):
        """更新上下文数据"""
        async with self.lock:
            if context_id in self.contexts:
                self.contexts[context_id].update(data)

    async def delete_context(self, context_id: str):
        """删除上下文"""
        async with self.lock:
            if context_id in self.contexts:
                del self.contexts[context_id]
