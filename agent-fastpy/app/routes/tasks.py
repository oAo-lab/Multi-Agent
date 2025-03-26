import asyncio
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import SessionLocal
from ..models.task import Interaction, Task
from ..schemas import Task as TaskSchema
from ..schemas import TaskCreate
from ..services.agent import agent_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tasks", response_model=List[TaskSchema])
async def list_tasks(query: str = "", db: Session = Depends(get_db)):
    tasks = db.query(Task)
    if query:
        tasks = tasks.filter(Task.name.contains(
            query) | Task.description.contains(query))
    return tasks.all()


@router.get("/tasks/{task_id}", response_model=TaskSchema)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: str, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.name = task.name
    db_task.description = task.description
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"status": "success", "message": "Task deleted"}


@router.post("/tasks", response_model=TaskSchema)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        name=task.name,
        description=task.description,
        status="created"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Define state transitions
ALLOWED_TRANSITIONS = {
    'created': ['pending'],
    'pending': ['running'],
    'running': ['completed', 'error', 'stopped'],
    'completed': [],
    'error': ['pending'],
    'stopped': ['pending']
}


def can_transition(current_status: str, new_status: str) -> bool:
    return new_status in ALLOWED_TRANSITIONS.get(current_status, [])


@router.get("/tasks/{task_id}/start")
async def start_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 检查任务状态
    if task.status == "running":
        raise HTTPException(status_code=400, detail="Task is already running")

    try:
        # Validate and set initializing state
        if not can_transition(task.status, "pending"):
            raise HTTPException(
                status_code=400, detail=f"Cannot transition from {task.status} to pending")

        task.status = "pending"
        db.commit()

        # 添加默认智能体，并初始化任务监控上下文
        task_str_id = str(task_id)
        task_message = task.description or task.name

        agent_service.add_agent(
            "前端开发", "资深前端工程师", task_str_id, task.name, task.description)
        agent_service.add_agent("UI设计师", "专业UI/UX设计师",
                                task_str_id, task.name, task.description)
        agent_service.add_agent(
            "代码审查", "高级代码审查员", task_str_id, task.name, task.description)

        # 启动任务并广播给智能体
        responses = await agent_service.broadcast_task(
            task_id,
            "前端开发",
            task_message
        )

        try:
            # Validate and set running state
            if not can_transition(task.status, "running"):
                raise HTTPException(
                    status_code=400, detail=f"Cannot transition from {task.status} to running")

            task.status = "running"

            # 批量添加交互记录
            interactions = [
                Interaction(
                    task_id=task_id,
                    sender="前端开发",
                    receiver=agent_name,
                    message=task_message,
                    response=response
                )
                for agent_name, response in responses.items()
            ]
            db.add_all(interactions)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to start task: {str(e)}")
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to start task: {str(e)}")

        # Start task processing in the background
        asyncio.create_task(process_task(task_id, task_message))

        return {"status": "success", "message": "Task started successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to start task: {str(e)}")


async def process_task(task_id: str, task_message: str):
    try:
        # Simulate task processing
        await asyncio.sleep(5)  # Simulate task duration

        # Update task status to 'completed' after processing
        db = SessionLocal()
        task = db.query(Task).filter(Task.id == task_id).first()
        if task and can_transition(task.status, "completed"):
            task.status = "completed"
            db.commit()

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to process task: {str(e)}")


@router.get("/tasks/{task_id}/stop")
async def stop_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Validate and set stopped state
    if not can_transition(task.status, "stopped"):
        raise HTTPException(
            status_code=400, detail=f"Cannot transition from {task.status} to stopped")

    task.status = "stopped"
    db.commit()
    return {"status": "success", "message": "Task stopped"}


@router.get("/tasks/{task_id}/history")
async def get_task_history(task_id: str, db: Session = Depends(get_db)):
    # Check if task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Fetch all interactions for the task
    interactions = db.query(Interaction).filter(
        Interaction.task_id == task_id).all()
    return interactions
