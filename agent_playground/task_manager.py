import asyncio
from typing import Dict, Optional

from agents.base import AgentBase
from context_manager import ContextManager  # 引入 ContextManager
from models.agent import Agent
from models.task import Task, TaskStatus, TaskStep, TaskStepStatus
from monitoring import log_event

MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 2  # 每次重试的间隔时间（秒）


class TaskManager:
    """任务管理器：负责任务调度、任务步骤执行、Agent 分配"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}  # 存储所有任务
        self.agents: Dict[str, AgentBase] = {}  # 存储所有注册的 Agent
        self.context_manager = ContextManager()  # 添加上下文管理器

    def register_agent(self, agent: AgentBase):
        """注册 Agent"""
        self.agents[agent.agent_id] = agent
        log_event("Agent Registered", f"Agent {agent.name} ({agent.role}) 已注册")

    async def create_task(self, name: str, steps: Dict[str, TaskStep]) -> Task:
        """创建任务，并分配上下文"""
        context_id = await self.context_manager.create_context()
        task = Task(name=name, steps=steps, context_id=context_id)
        self.tasks[task.task_id] = task
        log_event("Task Created", f"任务 {task.name} (ID: {task.task_id}) 创建成功")
        return task

    async def process_task(self, task_id: str):
        """处理任务调度，确保任务步骤的依赖顺序"""
        task = self.tasks.get(task_id)
        if not task:
            log_event("Task Not Found", f"任务 {task_id} 未找到", {"task_id": task_id})
            return

        log_event("Task Processing", f"开始处理任务: {task.name}")

        while task.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]:
            next_step = self._find_next_step(task)
            if not next_step:
                break  # 没有可执行的步骤，可能任务完成或被阻塞

            agent = self._find_suitable_agent(next_step.required_role)
            if agent:
                await self.execute_task_step(task, next_step, agent)
            else:
                log_event(
                    "Agent Not Found", f"没有找到合适的 Agent 执行 {next_step.name}"
                )
                await asyncio.sleep(2)  # 等待 Agent 空闲

        log_event("Task Completed", f"任务 {task.name} 处理完成")

    async def execute_task_step(self, task: Task, step: TaskStep, agent: AgentBase):
        """分配任务步骤给 Agent 并执行，同时支持错误重试"""
        step.status = TaskStepStatus.RUNNING
        step.assigned_agent_id = agent.agent_id
        agent.status = "busy"

        context = await self.context_manager.get_context(task.context_id)
        log_event("TaskStep Started", f"Agent {agent.name} 开始执行 {step.name}")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                result = await agent.execute_task(step, context)
                step.result = result
                step.status = TaskStepStatus.COMPLETED

                # 更新上下文
                if isinstance(result, dict):
                    await self.context_manager.update_context(task.context_id, result)

                log_event(
                    "TaskStep Completed",
                    f"任务步骤 {step.name} 执行完成",
                    {"result": result},
                )
                break  # 执行成功，跳出循环

            except Exception as e:
                log_event(
                    "TaskStep Failed",
                    f"任务步骤 {step.name} 第 {attempt} 次执行失败",
                    {"error": str(e)},
                )
                if attempt < MAX_RETRIES:
                    log_event(
                        "TaskStep Retry",
                        f"任务步骤 {step.name} 将在 {RETRY_DELAY} 秒后重试 ({attempt}/{MAX_RETRIES})",
                    )
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    step.status = TaskStepStatus.FAILED
                    log_event(
                        "TaskStep Gave Up", f"任务步骤 {step.name} 多次失败，放弃执行"
                    )

        agent.status = "idle"

    def _find_next_step(self, task: Task) -> Optional[TaskStep]:
        """查找下一个可执行的任务步骤（确保所有依赖已完成）"""
        for step in task.steps.values():
            if step.status == TaskStepStatus.PENDING:
                # 检查所有依赖步骤是否都已完成
                if all(
                    task.steps[dep].status == TaskStepStatus.COMPLETED
                    for dep in step.dependencies
                ):
                    return step
        return None

    def _find_suitable_agent(self, required_role: str) -> Optional[AgentBase]:
        """查找一个合适的 Agent"""
        for agent in self.agents.values():
            if agent.role == required_role and agent.status == "idle":
                return agent
        return None
