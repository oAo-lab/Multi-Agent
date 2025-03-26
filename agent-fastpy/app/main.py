from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .models import Base, engine
from .routes import tasks
from .services.agent import agent_service
from .services.websocket import websocket_manager

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化FastAPI应用
app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(tasks.router, prefix="/api")

# WebSocket连接处理
@app.websocket("/ws/tasks/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: int):
    try:
        await websocket_manager.connect(websocket, task_id)
        while True:
            try:
                # 保持连接活跃
                data = await websocket.receive_text()
            except WebSocketDisconnect:
                websocket_manager.disconnect(websocket, task_id)
                break
    except Exception as e:
        websocket_manager.disconnect(websocket, task_id)

# 初始化环境
@app.on_event("startup")
async def startup_event():
    await agent_service.initialize_environment()

@app.on_event("shutdown")
async def shutdown_event():
    await agent_service.close()