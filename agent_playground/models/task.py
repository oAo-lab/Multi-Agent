import uuid
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# 任务状态枚举
class TaskStatus(str, Enum):
    PENDING = "pending"  # 等待执行
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    BLOCKED = "blocked"  # 被阻塞


# 任务步骤状态枚举
class TaskStepStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# 任务步骤
class TaskStep(BaseModel):
    step_id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # 唯一标识
    name: str  # 步骤名称
    required_role: str  # 需要的 Agent 角色
    status: TaskStepStatus = TaskStepStatus.PENDING  # 步骤状态
    dependencies: List[str] = []  # 依赖的任务步骤 ID
    result: Optional[Any] = None  # 执行结果
    assigned_agent_id: Optional[str] = None  # 执行该步骤的 Agent ID


# 任务模型
class Task(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # 唯一标识
    name: str  # 任务名称
    status: TaskStatus = TaskStatus.PENDING  # 任务状态
    steps: Dict[str, TaskStep]  # 任务步骤，key 为 step_id
    context_id: Optional[str] = None  # 任务的上下文 ID
    result: Optional[Dict[str, Any]] = None  # 任务最终结果
    dependencies: List[str] = []  # 任务依赖的其他任务 ID
