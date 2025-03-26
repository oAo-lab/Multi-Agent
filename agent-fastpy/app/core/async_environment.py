from typing import Dict, List, Optional
from app.core.async_agent import AsyncAgent, PromptTemplate
import asyncio
from PIL import Image

class AsyncEnvironment:
    def __init__(self):
        self.agents: Dict[str, AsyncAgent] = {}
        self.interactions: List[Dict] = []
        self.prompt_templates: Dict[str, PromptTemplate] = {}
    
    async def initialize(self):
        """初始化所有智能体"""
        for agent in self.agents.values():
            await agent.initialize()
    
    async def close(self):
        """关闭所有智能体的会话"""
        for agent in self.agents.values():
            await agent.close()
    
    def add_agent(self, agent: AsyncAgent) -> None:
        """添加智能体到环境中"""
        self.agents[agent.name] = agent
    
    def remove_agent(self, agent_name: str) -> None:
        """从环境中移除智能体"""
        if agent_name in self.agents:
            del self.agents[agent_name]
    
    def get_agent(self, agent_name: str) -> Optional[AsyncAgent]:
        """获取指定名称的智能体"""
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[str]:
        """列出所有智能体的名称"""
        return list(self.agents.keys())
    
    def add_prompt_template(self, template: PromptTemplate) -> None:
        """添加提示词模板到环境"""
        self.prompt_templates[template.name] = template
        # 同步到所有智能体
        for agent in self.agents.values():
            agent.add_prompt_template(template)
    
    def get_prompt_template(self, name: str) -> Optional[PromptTemplate]:
        """获取提示词模板"""
        return self.prompt_templates.get(name)
    
    def list_prompt_templates(self) -> List[str]:
        """列出所有提示词模板"""
        return list(self.prompt_templates.keys())
    
    async def broadcast(self, sender: str, message: str) -> Dict[str, str]:
        """异步广播消息给所有其他智能体"""
        responses = {}
        sender_agent = self.agents.get(sender)
        if not sender_agent:
            return responses
        
        tasks = []
        for name, agent in self.agents.items():
            if name != sender:
                task = asyncio.create_task(sender_agent.interact(agent, message))
                tasks.append((name, task))
        
        for name, task in tasks:
            try:
                response = await task
                responses[name] = response
                self.interactions.append({
                    'sender': sender,
                    'receiver': name,
                    'message': message,
                    'response': response
                })
            except Exception as e:
                responses[name] = f"交互出错: {str(e)}"
        
        return responses
    
    async def process_image(self, image_path: str, processors: List[AsyncAgent]) -> Optional[Image.Image]:
        """多智能体协作处理图片"""
        current_image = None
        try:
            for processor in processors:
                if current_image is None:
                    current_image = await processor.process_image(image_path)
                else:
                    current_image = await processor.process_image(current_image)
            return current_image
        except Exception as e:
            print(f"图片处理出错: {str(e)}")
            return None
    
    def get_interaction_history(self) -> List[Dict]:
        """获取交互历史"""
        return self.interactions