from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    # 创建任务时只需要基本信息
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "name": "新任务",
                "description": "任务描述"
            }
        }

class Task(TaskBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InteractionBase(BaseModel):
    sender: str
    receiver: str
    message: str
    response: str

class Interaction(InteractionBase):
    id: str
    task_id: str
    created_at: datetime

    class Config:
        from_attributes = True