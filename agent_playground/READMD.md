## agent_playground

### 核心模块

- **agent_playground/**: 包含所有 Agent 及其相关支持模块。
  - **context_manager.py**: 管理任务的上下文信息，允许不同 Agent 共享数据。
  - **main.py**: 主程序入口，负责启动项目。
  - **monitoring.py**: 提供监控功能。
  - **task_manager.py**: 管理任务的生命周期。
  - **agents/**: 包含不同类型的 Agent。
    - **base.py**: 定义 Agent 的基础类。
    - **devops_engineer.py**: 模拟 DevOps 工程师的代理。
    - **llm_agent_base.py**: 定义与大语言模型集成的基础类。
    - **llm_integration.py**: 实现与大语言模型的集成。
    - **programmer.py**: 模拟程序员的代理。
    - **requirement_analyst.py**: 模拟需求分析师的代理。
    - **system_architect.py**: 模拟系统架构师的代理。
    - **tester.py**: 模拟测试人员的代理。
  - **models/**: 包含 Agent 和任务的模型定义。
    - **agent.py**: 定义 Agent 的模型。
    - **task.py**: 定义任务的模型。
- **breakthrough_design/**: 包含发布-订阅模式和异步任务池的实验。
  - **decorators/**: 包含异步装饰器示例。
    - **async_nomarl_with_dec.py**: 异步装饰器示例。
    - **async_with_dec.py**: 另一个异步装饰器示例。
  - **publish_subscribe_mode/**: 发布-订阅模式的实验。
    - **async_exp.py**: 发布-订阅模式的异步实现。
    - **async_task_pool_exp.py**: 异步任务池实验。
    - **synchronous_exp.py**: 发布-订阅模式的同步实现。
- **examples/**: 包含示例项目启动脚本。
  - **main.py**: 示例项目启动脚本。
- **prompts/**: 包含提示词工程的相关文档。
  - **提示词工程.md**: 关于提示词工程的文档。
  - **前端工程师/**: 前端工程师的提示词助手。
    - **tailwindcss+daysui 工程师-v1.md**: TailwindCSS 和 DaysUI 的前端工程师提示词助手。
    - **tailwindcss+daysui 工程师-v2.md**: 另一个版本的提示词助手。
  - **提示词生成/**: 提示词生成的相关文档。
    - **英文提示词助手-v1.md**: 英文提示词助手。
    - **中文提示词助手-v1.md**: 中文提示词助手。
    - **中文提示词助手-v2.md**: 另一个版本的中文提示词助手。

## 运行

- Install

  ```shell
  rye sync # or pip install
  ```

- run

  ```shell
  cd agent_playground
  python main.py
  ```