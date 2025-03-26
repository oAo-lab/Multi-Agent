import uuid
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


# 代理状态
class AgentStatus(str, Enum):
    IDLE = "idle"  # 空闲
    BUSY = "busy"  # 忙碌


# 代理模型
class Agent(BaseModel):
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # 唯一标识
    name: str  # 代理名称
    role: str  # 代理角色，例如 "RequirementAnalyst"
    status: AgentStatus = AgentStatus.IDLE  # 当前状态
    skills: List[str] = []  # 代理的技能

    model_config = {
        "arbitrary_types_allowed": True,
    }
