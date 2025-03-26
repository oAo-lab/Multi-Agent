# # agents/tester.py
# import asyncio
# import random
# from typing import Any, Dict, Optional

# from agents.base import AgentBase
# from models.task import TaskStep
# from monitoring import log_event


# class Tester(AgentBase):
#     """测试工程师 Agent"""

#     async def execute_task(
#         self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
#     ) -> Dict[str, str]:
#         log_event("Agent Execution", f"{self.name} 开始测试: {task_step.name}")
#         if context and "code" in context:
#             log_event("Context Received", f"{self.name} 发现代码: {context['code']}")
#         await asyncio.sleep(random.randint(3, 5))  # 模拟不同的测试时间
#         result = {"test_report": f"{task_step.name} 测试通过"}
#         log_event(
#             "Agent Completed",
#             f"{self.name} 任务完成: {task_step.name}",
#             {"result": result},
#         )
#         return result
# agents/tester.py
import asyncio
import random
from typing import Any, Dict, Optional

from agents.llm_agent_base import LLMAgentBase
from models.task import TaskStep
from monitoring import log_event


class Tester(LLMAgentBase):
    """测试工程师 Agent，使用 LLM 编写和执行测试"""

    system_prompt_backend: str = (
        "你是一位专业的测试工程师，请基于以下后端 API 代码编写全面的测试用例并执行测试。"
    )
    system_prompt_frontend: str = (
        "你是一位专业的测试工程师，请基于以下用户界面代码编写全面的测试用例并执行测试。"
    )
    default_llm_model: str = "qwen2.5-coder:1.5b"

    async def execute_task(
        self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        log_event("Agent Execution", f"{self.name} 开始测试: {task_step.name}")

        if task_step.name == "测试后端 API":
            backend_code = context.get("backend_code", "没有获取到后端 API 代码。")
            prompt = f"{self.system_prompt_backend}\n\n后端 API 代码：\n\n{backend_code}\n\n请输出测试结果。"
            llm_response = await self.call_llm(prompt=prompt)
            if (
                llm_response
                and llm_response.get("message")
                and llm_response["message"].get("content")
            ):
                test_report_backend = llm_response["message"]["content"]
                log_event(
                    "Agent Completed",
                    f"{self.name} 完成后端 API 测试",
                    {"test_report_backend": test_report_backend},
                )
                return {"test_report_backend": test_report_backend}
            else:
                raise Exception("后端 API 测试失败。")

        elif task_step.name == "测试用户界面":
            frontend_code = context.get("frontend_code", "没有获取到用户界面代码。")
            prompt = f"{self.system_prompt_frontend}\n\n用户界面代码：\n\n{frontend_code}\n\n请输出测试结果。"
            llm_response = await self.call_llm(prompt=prompt)
            if (
                llm_response
                and llm_response.get("message")
                and llm_response["message"].get("content")
            ):
                test_report_frontend = llm_response["message"]["content"]
                log_event(
                    "Agent Completed",
                    f"{self.name} 完成用户界面测试",
                    {"test_report_frontend": test_report_frontend},
                )
                return {"test_report_frontend": test_report_frontend}
            else:
                raise Exception("用户界面测试失败。")

        return {}
