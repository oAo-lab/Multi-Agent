# agents/requirement_analyst.py
from typing import Any, Dict, Optional

from agents.llm_agent_base import LLMAgentBase
from models.task import TaskStep
from monitoring import log_event


class RequirementAnalyst(LLMAgentBase):
    """需求分析师 Agent，使用 Ollama 模型进行需求分析"""

    system_prompt: str = "你是一位需求分析师, 请分析以下需求，提取关键功能点和用户期望."
    default_llm_model: str = "qwen2.5-coder:1.5b"
    task_info: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def append_task_info(self, msg: str):
        self.task_info = msg

    async def execute_task(
        self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        log_event(
            "Agent Execution", f"{self.name} 正在使用 LLM 分析需求: {self.task_info}"
        )

        llm_response = await self.call_llm(
            self.default_llm_model,
            messages=[
                self.llm_client.create_message("system", self.system_prompt),
            ],
            prompt=self.task_info,
        )

        if (
            llm_response
            and llm_response.get("message")
            and llm_response["message"].get("content")
        ):
            analysis_result = llm_response["message"]["content"]
            log_event(
                "Agent Completed",
                f"{self.name} LLM 分析完成: {task_step.name}",
                {"analysis": analysis_result},
            )
            return {"requirements": analysis_result}
        else:
            error_message = f"{self.name} 使用 LLM 分析需求失败: {task_step.name}"
            log_event("Agent Failed", error_message)
            raise Exception(error_message)
