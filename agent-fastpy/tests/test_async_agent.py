import unittest
import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from async_agent import AsyncAgent, PromptTemplate
from logger import Logger

class TestAsyncAgent(unittest.TestCase):
    def setUp(self):
        self.logger = Logger("test_agent")
        self.agent = AsyncAgent("test_agent", "测试助手")
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        if self.loop.is_running():
            self.loop.run_until_complete(self.agent.close())

    def test_initialization(self):
        """测试智能体初始化"""
        self.assertEqual(self.agent.name, "test_agent")
        self.assertEqual(self.agent.role, "测试助手")
        self.assertIsNotNone(self.agent.model)
        self.assertEqual(len(self.agent.memory), 0)

    def test_prompt_template_management(self):
        """测试提示词模板管理"""
        template = PromptTemplate(
            name="test_template",
            description="测试模板",
            template="这是一个测试模板 {param}",
            parameters={"param": "参数描述"}
        )
        self.agent.add_prompt_template(template)
        
        # 测试获取模板
        retrieved_template = self.agent.get_prompt_template("test_template")
        self.assertIsNotNone(retrieved_template)
        self.assertEqual(retrieved_template.name, "test_template")
        
        # 测试列出模板
        templates = self.agent.list_prompt_templates()
        self.assertIn("test_template", templates)

    def test_memory_operations(self):
        """测试记忆操作"""
        # 测试存储记忆
        self.agent.remember("test_key", "test_value")
        self.assertEqual(self.agent.recall("test_key"), "test_value")
        
        # 测试不存在的记忆
        self.assertIsNone(self.agent.recall("non_existent_key"))

    async def async_test_think(self):
        """测试思考功能"""
        await self.agent.initialize()
        response = await self.agent.think("你好")
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "")

    def test_think(self):
        """运行异步思考测试"""
        self.loop.run_until_complete(self.async_test_think())

if __name__ == "__main__":
    unittest.main()
