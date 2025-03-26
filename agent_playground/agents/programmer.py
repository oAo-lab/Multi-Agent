# # agents/programmer.py
# import asyncio
# import random
# from typing import Any, Dict, Optional

# from agents.base import AgentBase
# from models.task import TaskStep
# from monitoring import log_event


# class Programmer(AgentBase):
#     """程序员 Agent"""

#     async def execute_task(
#         self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
#     ) -> Dict[str, str]:
#         log_event("Agent Execution", f"{self.name} 开始编码: {task_step.name}")
#         if context and "architecture" in context:
#             log_event(
#                 "Context Received", f"{self.name} 读取架构: {context['architecture']}"
#             )
#         await asyncio.sleep(random.randint(2, 4))  # 模拟不同的编码时间
#         result = {"code": f"{task_step.name} 代码实现完成"}
#         log_event(
#             "Agent Completed",
#             f"{self.name} 任务完成: {task_step.name}",
#             {"result": result},
#         )
#         return result
# agents/programmer.py
import os
import re
from typing import Any, Dict, Optional

from agents.llm_agent_base import LLMAgentBase
from models.task import TaskStep
from monitoring import log_event


def init_prompt() -> str:
    system_prompt_frontend = ""
    with open(
        "../prompts/前端工程师/tailwindcss+daysui工程师-v1.md", "r", encoding="utf-8"
    ) as fp:
        system_prompt_frontend = fp.read()
    return system_prompt_frontend


def extract_html_code_blocks_from_markdown(
    markdown_content, output_dir="extracted_html"
):
    """
    从 Markdown 内容中提取所有的 HTML 代码块，并保存到指定目录下的单独文件中。

    :param markdown_content: str, Markdown 文件的内容
    :param output_dir: str, 存储提取的 HTML 代码块的目录，默认为 "extracted_html"
    """
    # 创建输出目录（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 正则表达式匹配代码块
    code_block_pattern = r"```(html)?\s*(.*?)\s*```"

    # 查找所有匹配的代码块
    matches = re.findall(
        code_block_pattern, markdown_content, re.DOTALL | re.IGNORECASE
    )

    # 遍历匹配结果并保存每个 HTML 代码块
    for idx, match in enumerate(matches, start=1):
        language, code = match
        language = (language or "").strip().lower()  # 获取语言标识符并规范化

        # 检查是否是 HTML 代码块
        if language == "html":
            # 移除多余的换行符
            code = code.strip()

            # 构建输出文件路径
            file_name = f"html_code_block_{idx}.html"
            file_path = os.path.join(output_dir, file_name)

            # 将代码块写入文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            print(f"已提取并保存: {file_path}")


class Programmer(LLMAgentBase):
    """程序员 Agent，使用 LLM 实现代码"""

    system_prompt_backend: str = (
        "你是一位熟练的后端工程师，请根据以下系统架构和数据库模型实现后端 API。"
    )
    system_prompt_frontend: str = (
        # "你是一位专业的前端工程师，请根据以下系统架构和用户界面设计实现用户界面代码。"
        init_prompt()
    )
    default_llm_model: str = "qwen2.5-coder:1.5b"

    async def execute_task(
        self, task_step: TaskStep, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        log_event("Agent Execution", f"{self.name} 开始编码: {task_step.name}")

        log_event("system_prompt_frontend: ", self.system_prompt_frontend)

        if task_step.name == "实现后端 API":
            architecture = context.get("architecture", "没有获取到系统架构信息。")
            database_model = context.get("database_model", "没有获取到数据库模型信息。")
            prompt = f"{self.system_prompt_backend}\n\n系统架构：{architecture}\n\n数据库模型：{database_model}"
            llm_response = await self.call_llm(prompt=prompt)
            if (
                llm_response
                and llm_response.get("message")
                and llm_response["message"].get("content")
            ):
                backend_code = llm_response["message"]["content"]
                log_event(
                    "Agent Completed",
                    f"{self.name} 完成后端 API 实现",
                    {"backend_code": backend_code},
                )
                return {"backend_code": backend_code}
            else:
                raise Exception("后端 API 实现失败。")

        elif task_step.name == "实现用户界面":
            architecture = context.get("architecture", "没有获取到系统架构信息。")
            # 可以假设前端设计稿也通过某种方式传递，这里简化处理
            prompt = f"{self.system_prompt_frontend}\n\n系统架构：{architecture}\n\n请实现用户注册和登录相关的用户界面。"
            llm_response = await self.call_llm(prompt=prompt)
            if (
                llm_response
                and llm_response.get("message")
                and llm_response["message"].get("content")
            ):
                frontend_code = llm_response["message"]["content"]
                log_event(
                    "Agent Completed",
                    f"{self.name} 完成用户界面实现",
                    {"frontend_code": frontend_code},
                )
                extract_html_code_blocks_from_markdown(frontend_code)
                return {"frontend_code": frontend_code}
            else:
                raise Exception("用户界面实现失败。")

        return {}
