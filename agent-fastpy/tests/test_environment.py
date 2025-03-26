import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from async_agent import AsyncAgent, PromptTemplate
from async_environment import AsyncEnvironment
from logger import Logger


class TestAsyncEnvironment(unittest.TestCase):
    def setUp(self):
        self.logger = Logger("test_environment")
        self.env = AsyncEnvironment()
        self.loop = asyncio.get_event_loop()
        self.agent1 = AsyncAgent("agent1", "助手1")
        self.agent2 = AsyncAgent("agent2", "助手2")

    def tearDown(self):
        if self.loop.is_running():
            self.loop.run_until_complete(self.env.close())

    def test_agent_management(self):
        """测试智能体管理功能"""
        self.env.add_agent(self.agent1)
        self.env.add_agent(self.agent2)

        # 测试获取智能体
        self.assertEqual(len(self.env.list_agents()), 2)
        self.assertIsNotNone(self.env.get_agent("agent1"))
        self.assertIsNotNone(self.env.get_agent("agent2"))

        # 测试移除智能体
        self.env.remove_agent("agent1")
        self.assertEqual(len(self.env.list_agents()), 1)
        self.assertIsNone(self.env.get_agent("agent1"))

    def test_prompt_template_management(self):
        """测试提示词模板管理"""
        template = PromptTemplate(
            name="test_template",
            description="测试模板",
            template="这是一个测试模板 {param}",
            parameters={"param": "参数描述"},
        )
        self.env.add_prompt_template(template)

        # 测试获取模板
        retrieved_template = self.env.get_prompt_template("test_template")
        self.assertIsNotNone(retrieved_template)
        self.assertEqual(retrieved_template.name, "test_template")

        # 测试列出模板
        templates = self.env.list_prompt_templates()
        self.assertIn("test_template", templates)

    async def async_test_broadcast(self):
        """测试广播功能"""
        self.env.add_agent(self.agent1)
        self.env.add_agent(self.agent2)
        await self.env.initialize()

        responses = await self.env.broadcast("agent1", "测试消息")
        self.assertIn("agent2", responses)
        self.assertIsInstance(responses["agent2"], str)

    def test_broadcast(self):
        """运行异步广播测试"""
        self.loop.run_until_complete(self.async_test_broadcast())

    def test_interaction_history(self):
        """测试交互历史记录"""
        self.env.add_agent(self.agent1)
        self.env.add_agent(self.agent2)

        # 运行一些交互
        self.loop.run_until_complete(self.async_test_broadcast())

        # 检查历史记录
        history = self.env.get_interaction_history()
        self.assertGreater(len(history), 0)
        self.assertIn("sender", history[0])
        self.assertIn("receiver", history[0])
        self.assertIn("message", history[0])
        self.assertIn("response", history[0])


if __name__ == "__main__":
    unittest.main()
