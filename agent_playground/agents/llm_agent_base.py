# agents/llm_agent_base.py
from abc import ABC
from typing import Any, Dict, List, Optional

from agents.base import AgentBase
from agents.llm_integration import OllamaClientWrapper


class LLMAgentBase(AgentBase, ABC):
    """继承自 AgentBase, 为需要 LLM 功能的 Agent 提供基础"""

    llm_client: OllamaClientWrapper = OllamaClientWrapper()
    default_llm_model: str = "llama3.2"  # 可以设置默认模型

    async def call_llm(
        self,
        model: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        prompt: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """封装 LLM 调用逻辑"""
        model_to_use = model if model else self.default_llm_model
        messages_to_use = messages if messages else []
        if prompt:
            messages_to_use.append(self.llm_client.create_message("user", prompt))
        if not messages_to_use:
            raise ValueError("No messages or prompt provided for LLM call.")
        return await self.llm_client.chat(model=model_to_use, messages=messages_to_use)
