# llm_integration.py
from typing import Any, Dict, List, Optional

from monitoring import log_event
from ollama import AsyncClient


class OllamaClientWrapper:
    """
    封装 Ollama AsyncClient, 提供更便捷的接口和日志记录。
    """

    def __init__(self, base_url: Optional[str] = None):
        self.client = AsyncClient()

    async def chat(
        self, model: str, messages: List[Dict[str, str]], stream: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        与 Ollama 模型进行非流式对话。
        """
        try:
            # log_event(
            #     "LLM Interaction", f"Calling model '{model}'", {"messages": messages}
            # )
            response = await self.client.chat(
                model=model, messages=messages, stream=stream
            )
            # log_event(
            #     "LLM Response Received",
            #     f"Response from '{model}'",
            #     {"response": response.model_dump()},
            # )
            return response.model_dump()
        except Exception as e:
            log_event(
                "LLM Interaction Error",
                f"Error calling model '{model}'",
                {"error": str(e), "messages": messages},
            )
            return None

    def create_message(self, role: str, content: str) -> Dict[str, str]:
        """
        创建符合 Ollama 消息格式的消息。
        """
        return {"role": role, "content": content}
