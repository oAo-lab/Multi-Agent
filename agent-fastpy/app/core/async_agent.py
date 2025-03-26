# 标准库
import asyncio
from typing import Any, Dict, List, Optional

# 第三方库
import aiohttp
import dashscope
from PIL import Image
from pydantic import BaseModel

# 本地模块
from .config import config
from .logger import Logger
from .monitor import monitor


class PromptTemplate(BaseModel):
    """提示词模板"""

    name: str
    description: str
    template: str
    parameters: Dict[str, str] = {}


class AsyncAgent:
    def __init__(self, name: str, role: str):
        self.logger = Logger(f"Agent.{name}")
        self.name = name
        self.role = role
        self.memory: Dict[str, Any] = {}
        
        if not config.dashscope_api_key:
            raise ValueError("DASHSCOPE_API_KEY 未配置")
            
        dashscope.api_key = config.dashscope_api_key
        self.model = dashscope.Generation()
        self.prompt_templates: Dict[str, PromptTemplate] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
        self.logger.info(f"初始化智能体 {name}，角色：{role}")
        monitor.log_event("agent_init", f"初始化智能体：{name} ({role})")

    async def initialize(self):
        """初始化异步会话"""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """关闭异步会话"""
        if self.session:
            await self.session.close()
            self.session = None

    async def think(self, context: str) -> str:
        """异步思考并生成回应"""
        monitor.log_event("agent_think_start", f"智能体 {self.name} 开始思考")
        try:
            response = await asyncio.to_thread(
                self.model.call,
                dashscope.Generation.Models.qwen_turbo,
                messages=[
                    {
                        "role": "system",
                        "content": f"你是一个名为{self.name}的AI助手，扮演{self.role}的角色。",
                    },
                    {"role": "user", "content": context},
                ],
            )
            
            # 记录思考结果
            monitor.add_artifact(
                "agent_thought",
                f"# {self.name} 的思考结果\n\n**上下文**:\n{context}\n\n**回应**:\n{response.output.text}",
                {
                    "agent": self.name,
                    "role": self.role
                }
            )
            
            monitor.log_event("agent_think_end", f"智能体 {self.name} 完成思考")
            return response.output.text
        except Exception as e:
            error_msg = f"思考时出错: {str(e)}"
            monitor.log_event("agent_think_error", error_msg)
            return error_msg

    def add_prompt_template(self, template: PromptTemplate) -> None:
        """添加提示词模板"""
        self.prompt_templates[template.name] = template
        monitor.log_event("template_added", f"添加模板：{template.name}")
        monitor.add_artifact(
            "prompt_template",
            f"# 提示词模板：{template.name}\n\n**描述**: {template.description}\n\n**模板内容**:\n{template.template}",
            {
                "template_name": template.name,
                "parameters": template.parameters
            }
        )

    def get_prompt_template(self, name: str) -> Optional[PromptTemplate]:
        """获取提示词模板"""
        template = self.prompt_templates.get(name)
        if template:
            monitor.log_event("template_retrieved", f"获取模板：{name}")
        return template

    def list_prompt_templates(self) -> List[str]:
        """列出所有提示词模板"""
        templates = list(self.prompt_templates.keys())
        monitor.log_event("template_listed", f"列出所有模板，共 {len(templates)} 个")
        return templates

    async def process_image(self, image_path: str) -> Optional[Image.Image]:
        """处理图片"""
        try:
            with Image.open(image_path) as img:
                return img.copy()
        except Exception as e:
            print(f"处理图片时出错: {str(e)}")
            return None

    def remember(self, key: str, value: Any) -> None:
        """记忆信息"""
        self.memory[key] = value
        monitor.log_event("memory_added", f"添加记忆：{key}")
        monitor.add_artifact(
            "memory",
            f"# 记忆信息\n\n**键**: {key}\n\n**值**:\n{value}",
            {
                "key": key,
                "value_type": type(value).__name__
            }
        )

    def recall(self, key: str) -> Optional[Any]:
        """回忆信息"""
        value = self.memory.get(key)
        if value:
            monitor.log_event("memory_retrieved", f"回忆记忆：{key}")
        return value

    async def interact(self, other_agent: "AsyncAgent", message: str) -> str:
        """与其他智能体异步交互"""
        monitor.log_event("agent_interaction_start", 
                        f"{self.name} 开始与 {other_agent.name} 交互")
        
        context = f"来自{self.name}的消息：{message}"
        response = await other_agent.think(context)
        
        monitor.log_event("agent_interaction_end", 
                        f"{self.name} 与 {other_agent.name} 交互完成")
        
        monitor.add_artifact(
            "agent_interaction",
            f"# 智能体交互\n\n**发起者**: {self.name}\n\n**接收者**: {other_agent.name}\n\n**消息**:\n{message}\n\n**回应**:\n{response}",
            {
                "sender": self.name,
                "receiver": other_agent.name
            }
        )
        
        return response
