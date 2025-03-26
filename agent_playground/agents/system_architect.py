# import asyncio
# from typing import Any, Dict, Optional

# from agents.base import AgentBase
# from models.task import TaskStep
# from monitoring import log_event


# class SystemArchitect(AgentBase):
#     """系统架构师 Agent"""

#     async def execute_task(
#         self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
#     ) -> Dict[str, str]:
#         log_event("Agent Execution", f"{self.name} 开始设计架构: {task_step.name}")

#         if context and "requirements" in context:
#             log_event(
#                 "Context Received", f"{self.name} 读取需求: {context['requirements']}"
#             )

#         await asyncio.sleep(2)
#         result = {"architecture": f"{task_step.name} 设计完成"}
#         log_event(
#             "Agent Completed",
#             f"{self.name} 任务完成: {task_step.name}",
#             {"result": result},
#         )
#         return result
# agents/system_architect.py
import asyncio
from typing import Any, Dict, Optional

from agents.llm_agent_base import LLMAgentBase
from models.task import TaskStep
from monitoring import log_event


class SystemArchitect(LLMAgentBase):
    """系统架构师 Agent，使用 LLM 设计系统架构和数据库模型"""

    system_prompt_architecture: str = (
        "你是一位经验丰富的系统架构师，请基于以下需求设计一个高可用的系统架构。"
    )
    system_prompt_database: str = (
        "你是一位数据库专家，请基于以下需求和系统架构设计详细的数据库模型。"
    )
    default_llm_model: str = "qwen2.5-coder:1.5b"

    async def execute_task(
        self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        log_event("Agent Execution", f"{self.name} 开始设计: {task_step.name}")

        if task_step.name == "设计系统架构":
            requirements = context.get("requirements", "没有获取到需求信息。")
            prompt = f"{self.system_prompt_architecture}\n\n需求：{requirements}"
            llm_response = await self.call_llm(prompt=prompt)
            if (
                llm_response
                and llm_response.get("message")
                and llm_response["message"].get("content")
            ):
                architecture = llm_response["message"]["content"]
                log_event(
                    "Agent Completed",
                    f"{self.name} 完成架构设计",
                    {"architecture": architecture},
                )
                return {"architecture": architecture}
            else:
                raise Exception("架构设计失败。")

        elif task_step.name == "设计数据库模型":
            requirements = context.get("requirements", "没有获取到需求信息。")
            architecture = context.get("architecture", "没有获取到系统架构信息。")
            prompt = f"{self.system_prompt_database}\n\n需求：{requirements}\n\n系统架构：{architecture}"
            llm_response = await self.call_llm(prompt=prompt)
            if (
                llm_response
                and llm_response.get("message")
                and llm_response["message"].get("content")
            ):
                database_model = llm_response["message"]["content"]
                log_event(
                    "Agent Completed",
                    f"{self.name} 完成数据库模型设计",
                    {"database_model": database_model},
                )
                return {"database_model": database_model}
            else:
                raise Exception("数据库模型设计失败。")

        return {}
