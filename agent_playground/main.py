"""
# 测试 Agent 创建
from models.agent import Agent, AgentStatus
from models.task import Task, TaskStatus, TaskStep

# 创建一个任务步骤
step1 = TaskStep(name="分析需求", required_role="RequirementAnalyst")
step2 = TaskStep(
    name="设计架构", required_role="SystemArchitect", dependencies=[step1.step_id]
)

# 创建任务
task = Task(name="开发电商平台", steps={step1.step_id: step1, step2.step_id: step2})

# 创建代理
agent = Agent(name="张三", role="RequirementAnalyst")

print(task)
print()
print(agent)
"""

""" 
# 测试 Agent do Task
import asyncio

from agents.requirement_analyst import RequirementAnalyst
from models.task import TaskStep


async def test_agent():
    step = TaskStep(name="分析需求", required_role="RequirementAnalyst")
    agent = RequirementAnalyst(name="张三", role="RequirementAnalyst")

    result = await agent.execute_task(step)
    print(f"执行结果: {result}")


asyncio.run(test_agent())
"""

""" 
# 测试任务步骤是否正确
import asyncio

from agents.requirement_analyst import RequirementAnalyst
from models.task import TaskStep
from task_manager import TaskManager


async def test_task_manager():
    manager = TaskManager()

    # 注册 Agent
    agent = RequirementAnalyst(name="张三", role="RequirementAnalyst")
    manager.register_agent(agent)

    # 创建任务步骤
    step1 = TaskStep(name="分析需求", required_role="RequirementAnalyst")
    step2 = TaskStep(
        name="设计架构", required_role="SystemArchitect", dependencies=[step1.step_id]
    )

    # 创建任务
    task = manager.create_task(
        "开发电商平台", steps={step1.step_id: step1, step2.step_id: step2}
    )

    # 处理任务
    await manager.process_task(task.task_id)


asyncio.run(test_task_manager())
"""


""" 
# 判断是否能正确执行
import asyncio

from agents.requirement_analyst import RequirementAnalyst
from agents.system_architect import SystemArchitect
from models.task import TaskStep
from task_manager import TaskManager


async def test_task_manager():
    manager = TaskManager()

    # 注册 Agents
    analyst = RequirementAnalyst(name="张三", role="RequirementAnalyst")
    architect = SystemArchitect(name="李四", role="SystemArchitect")

    manager.register_agent(analyst)
    manager.register_agent(architect)

    # 创建任务步骤
    step1 = TaskStep(name="分析需求", required_role="RequirementAnalyst")
    step2 = TaskStep(
        name="设计架构", required_role="SystemArchitect", dependencies=[step1.step_id]
    )

    # 创建任务
    task = await manager.create_task(
        "开发电商平台", steps={step1.step_id: step1, step2.step_id: step2}
    )

    # 处理任务
    await manager.process_task(task.task_id)


asyncio.run(test_task_manager())
"""

""" 
# 依赖关系实现
import asyncio

from agents.requirement_analyst import RequirementAnalyst
from agents.system_architect import SystemArchitect
from models.task import TaskStep
from task_manager import TaskManager


async def test_task_dependencies():
    manager = TaskManager()

    # 注册 Agents
    analyst = RequirementAnalyst(name="张三", role="RequirementAnalyst")
    architect = SystemArchitect(name="李四", role="SystemArchitect")

    manager.register_agent(analyst)
    manager.register_agent(architect)

    # 创建任务步骤（设计架构依赖分析需求，编码实现依赖设计架构）
    step1 = TaskStep(name="分析需求", required_role="RequirementAnalyst")
    step2 = TaskStep(
        name="设计架构", required_role="SystemArchitect", dependencies=[step1.step_id]
    )
    # step3 = TaskStep(
    #     name="编码实现", required_role="Programmer", dependencies=[step2.step_id]
    # )

    # 创建任务
    task = await manager.create_task(
        "开发电商平台",
        steps={step1.step_id: step1, step2.step_id: step2},
        #  step3.step_id: step3
    )

    # 处理任务
    await manager.process_task(task.task_id)


asyncio.run(test_task_dependencies())
"""

"""
# 测试多流程步骤执行
import asyncio
import random

from agents.devops_engineer import DevOpsEngineer
from agents.programmer import Programmer
from agents.requirement_analyst import RequirementAnalyst
from agents.system_architect import SystemArchitect
from agents.tester import Tester
from models.task import TaskStep
from monitoring import log_event
from task_manager import TaskManager


async def test_complex_task():
    manager = TaskManager()

    # 注册 Agents
    analyst = RequirementAnalyst(name="Alice", role="RequirementAnalyst")
    architect = SystemArchitect(name="Bob", role="SystemArchitect")
    programmer1 = Programmer(name="Charlie", role="Programmer")
    programmer2 = Programmer(name="David", role="Programmer")
    tester = Tester(name="Eve", role="Tester")
    devops = DevOpsEngineer(name="Frank", role="DevOpsEngineer")

    manager.register_agent(analyst)
    manager.register_agent(architect)
    manager.register_agent(programmer1)
    manager.register_agent(programmer2)
    manager.register_agent(tester)
    manager.register_agent(devops)

    # 创建更复杂的任务步骤
    step_req_analysis = TaskStep(
        name="分析用户故事", required_role="RequirementAnalyst"
    )
    step_arch_design = TaskStep(
        name="设计系统架构",
        required_role="SystemArchitect",
        dependencies=[step_req_analysis.step_id],
    )
    step_db_design = TaskStep(
        name="设计数据库模型",
        required_role="SystemArchitect",
        dependencies=[step_req_analysis.step_id],
    )
    step_backend_coding = TaskStep(
        name="实现后端 API",
        required_role="Programmer",
        dependencies=[step_arch_design.step_id, step_db_design.step_id],
    )
    step_frontend_coding = TaskStep(
        name="实现用户界面",
        required_role="Programmer",
        dependencies=[step_arch_design.step_id],
    )
    step_backend_testing = TaskStep(
        name="测试后端 API",
        required_role="Tester",
        dependencies=[step_backend_coding.step_id],
    )
    step_frontend_testing = TaskStep(
        name="测试用户界面",
        required_role="Tester",
        dependencies=[step_frontend_coding.step_id],
    )
    step_deployment = TaskStep(
        name="部署应用程序",
        required_role="DevOpsEngineer",
        dependencies=[step_backend_testing.step_id, step_frontend_testing.step_id],
    )

    # 创建任务
    task = await manager.create_task(
        "构建社交媒体应用",
        steps={
            step_req_analysis.step_id: step_req_analysis,
            step_arch_design.step_id: step_arch_design,
            step_db_design.step_id: step_db_design,
            step_backend_coding.step_id: step_backend_coding,
            step_frontend_coding.step_id: step_frontend_coding,
            step_backend_testing.step_id: step_backend_testing,
            step_frontend_testing.step_id: step_frontend_testing,
            step_deployment.step_id: step_deployment,
        },
    )

    # 处理任务
    await manager.process_task(task.task_id)


if __name__ == "__main__":
    asyncio.run(test_complex_task())
"""

"""
# 单任务测试
import asyncio

from agents.requirement_analyst import RequirementAnalyst
from models.task import TaskStep
from monitoring import log_event
from task_manager import TaskManager


async def test_ollama_integration():
    manager = TaskManager()

    # 注册 RequirementAnalyst Agent
    analyst = RequirementAnalyst(name="Alice", role="RequirementAnalyst")
    manager.register_agent(analyst)

    # 创建一个需要需求分析的任务步骤
    step_analyze_feature = TaskStep(
        name="用户注册和登录功能", required_role="RequirementAnalyst"
    )

    # 创建任务
    task = await manager.create_task(
        "分析新功能需求", steps={step_analyze_feature.step_id: step_analyze_feature}
    )

    # 处理任务
    await manager.process_task(task.task_id)


if __name__ == "__main__":
    asyncio.run(test_ollama_integration())
"""

# 测试多流程步骤集成LLM执行
import asyncio

from agents.devops_engineer import DevOpsEngineer
from agents.programmer import Programmer
from agents.requirement_analyst import RequirementAnalyst
from agents.system_architect import SystemArchitect
from agents.tester import Tester
from models.task import TaskStep
from task_manager import TaskManager


async def test_complex_task():
    manager = TaskManager()

    # 注册 Agents
    analyst = RequirementAnalyst(name="Alice", role="RequirementAnalyst")
    architect = SystemArchitect(name="Bob", role="SystemArchitect")
    programmer1 = Programmer(name="Charlie", role="Programmer")
    programmer2 = Programmer(name="David", role="Programmer")
    tester = Tester(name="Eve", role="Tester")
    devops = DevOpsEngineer(name="Frank", role="DevOpsEngineer")

    manager.register_agent(analyst)
    manager.register_agent(architect)
    manager.register_agent(programmer1)
    manager.register_agent(programmer2)
    manager.register_agent(tester)
    manager.register_agent(devops)

    # 创建更复杂的任务步骤
    step_req_analysis = TaskStep(
        name="分析用户故事", required_role="RequirementAnalyst"
    )
    step_arch_design = TaskStep(
        name="设计系统架构",
        required_role="SystemArchitect",
        dependencies=[step_req_analysis.step_id],
    )
    step_db_design = TaskStep(
        name="设计数据库模型",
        required_role="SystemArchitect",
        dependencies=[step_req_analysis.step_id],
    )
    step_backend_coding = TaskStep(
        name="实现后端 API",
        required_role="Programmer",
        dependencies=[
            step_arch_design.step_id,
            step_db_design.step_id,
            step_req_analysis.step_id,
        ],
    )
    step_frontend_coding = TaskStep(
        name="实现用户界面",
        required_role="Programmer",
        dependencies=[
            step_arch_design.step_id,
            step_req_analysis.step_id,
            step_db_design.step_id,
        ],
    )
    step_backend_testing = TaskStep(
        name="测试后端 API",
        required_role="Tester",
        dependencies=[step_backend_coding.step_id],
    )
    step_frontend_testing = TaskStep(
        name="测试用户界面",
        required_role="Tester",
        dependencies=[step_frontend_coding.step_id],
    )
    step_deployment = TaskStep(
        name="部署应用程序",
        required_role="DevOpsEngineer",
        dependencies=[step_backend_testing.step_id, step_frontend_testing.step_id],
    )

    analyst.append_task_info(
        "编写一个影视系统，需要包含如下页面: 影视主页，影视搜索页，影视详情页，登录注册页，采用tailwindcss做。后端采用Go的Gin来编写，并采用gorm和sqlite做数据方面的，前端需要采用axios来做数据传递。"
    )

    # 创建任务
    task = await manager.create_task(
        analyst.task_info,
        steps={
            step_req_analysis.step_id: step_req_analysis,
            step_arch_design.step_id: step_arch_design,
            step_db_design.step_id: step_db_design,
            step_backend_coding.step_id: step_backend_coding,
            step_frontend_coding.step_id: step_frontend_coding,
            step_backend_testing.step_id: step_backend_testing,
            step_frontend_testing.step_id: step_frontend_testing,
            step_deployment.step_id: step_deployment,
        },
    )

    # 处理任务
    await manager.process_task(task.task_id)


if __name__ == "__main__":
    asyncio.run(test_complex_task())
