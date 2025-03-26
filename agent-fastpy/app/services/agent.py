from typing import Dict, List, Optional
from app.core.async_agent import AsyncAgent
from app.core.async_environment import AsyncEnvironment
from app.core.monitor import monitor
from .websocket import websocket_manager

class AgentService:
    def __init__(self):
        self._environment: Optional[AsyncEnvironment] = None
        self._agents: Dict[str, AsyncAgent] = {}

    async def initialize_environment(self):
        """初始化异步环境"""
        self._environment = AsyncEnvironment()
        await self._environment.initialize()

    def add_agent(self, name: str, role: str, task_id: str = None, task_name: str = None, task_description: str = None) -> AsyncAgent:
        """添加智能体到环境"""
        # 如果提供了任务信息，初始化监控上下文
        if task_id and task_name:
            monitor.initialize_task(task_id, task_name, task_description or task_name)
            monitor.register_agent(task_id, name, role)
            
        agent = AsyncAgent(name, role)
        self._agents[name] = agent
        if self._environment:
            self._environment.add_agent(agent)
        return agent

    async def broadcast_task(self, task_id: int, sender: str, message: str) -> Dict[str, str]:
        """广播任务给所有智能体"""
        if not self._environment:
            raise RuntimeError("Environment not initialized")

        # 记录任务开始
        monitor.log_event("task_start", f"开始任务: {message}")
        monitor.add_artifact("task_description", f"# 任务描述\n\n{message}")

        # 广播消息
        responses = await self._environment.broadcast(sender, message)

        # 记录智能体响应
        for agent_name, response in responses.items():
            monitor.add_artifact(
                "agent_response",
                f"# {agent_name}的建议\n\n{response}",
                {"agent": agent_name}
            )
            # 通过WebSocket发送响应
            await websocket_manager.broadcast_to_task(
                task_id,
                {
                    "type": "agent_response",
                    "agent": agent_name,
                    "response": response
                }
            )

        return responses

    def get_interaction_history(self) -> List[Dict]:
        """获取交互历史"""
        if not self._environment:
            return []
        return self._environment.get_interaction_history()

    async def close(self):
        """关闭环境和智能体"""
        if self._environment:
            await self._environment.close()
            self._environment = None
            self._agents.clear()

agent_service = AgentService()