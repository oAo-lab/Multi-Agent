# # agents/devops_engineer.py
# import asyncio
# import random
# from typing import Any, Dict, Optional

# from agents.base import AgentBase
# from models.task import TaskStep
# from monitoring import log_event


# class DevOpsEngineer(AgentBase):
#     """DevOps 工程师 Agent"""

#     async def execute_task(
#         self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
#     ) -> Dict[str, str]:
#         log_event("Agent Execution", f"{self.name} 开始部署: {task_step.name}")
#         if context and "code" in context:
#             log_event("Context Received", f"{self.name} 部署代码: {context['code']}")
#         await asyncio.sleep(random.randint(4, 6))  # 模拟不同的部署时间
#         result = {"deployment_status": f"{task_step.name} 部署成功"}
#         log_event(
#             "Agent Completed",
#             f"{self.name} 任务完成: {task_step.name}",
#             {"result": result},
#         )
#         return result
# agents/devops_engineer.py
import asyncio
import random
from typing import Any, Dict, Optional

from agents.base import AgentBase  # DevOps 通常不直接使用 LLM 进行部署
from models.task import TaskStep
from monitoring import log_event


class DevOpsEngineer(AgentBase):
    """DevOps 工程师 Agent，负责部署应用"""

    async def execute_task(
        self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        log_event("Agent Execution", f"{self.name} 开始部署: {task_step.name}")

        if task_step.name == "部署应用程序":
            backend_report = context.get(
                "test_report_backend", "没有获取到后端测试报告。"
            )
            frontend_report = context.get(
                "test_report_frontend", "没有获取到前端测试报告。"
            )
            backend_code = context.get("backend_code", "没有获取到后端代码。")
            frontend_code = context.get("frontend_code", "没有获取到前端代码。")

            log_event(
                "Context Received",
                f"{self.name} 准备部署",
                {
                    "backend_report": backend_report,
                    "frontend_report": frontend_report,
                    "backend_code": backend_code[:50] if backend_code else "...",
                    "frontend_code": frontend_code[:50] if frontend_code else "...",
                },
            )

            await asyncio.sleep(random.randint(5, 8))  # 模拟部署时间
            deployment_status = (
                "部署成功"
                if "通过" in backend_report and "通过" in frontend_report
                else "部署失败，测试未通过"
            )
            log_event(
                "Agent Completed",
                f"{self.name} 完成部署",
                {"deployment_status": deployment_status},
            )
            return {"deployment_status": deployment_status}

        return {}
