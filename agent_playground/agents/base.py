from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from models.agent import Agent
from models.task import TaskStep


class AgentBase(Agent, ABC):
    """抽象基类，所有 Agent 需要继承并实现 execute_task 方法"""

    @abstractmethod
    async def execute_task(
        self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """执行任务步骤，返回执行结果"""
        pass
