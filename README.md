# Multi-Agent Workflow Project

[中文文档](README.zh-CN.md)

## Project Overview

This project aims to implement a multi-agent system that handles complex multi-process tasks by integrating with local Ollama interfaces. Each agent focuses on a different role, such as DevOps Engineer, Programmer, Requirements Analyst, etc., and they collaborate by sharing context information. The project also explores asynchronous programming techniques to improve system responsiveness and efficiency.

## Project Motivation

> With the development of AI, multi-agent collaboration to complete various tasks is an inevitable trend. This project aims to realize various ideas in mind and strive to implement a multi-process Agent system. It designs an architectural system and implements it in Go, Python, and low-code workflows. The implementation details vary, but the core logic is similar. With continuous practice, it is found that the complexity of writing the entire process in pure code will increase, especially when various cloud model calls take too long. The system needs to be reliable and traceable. Practice shows that using the MCP protocol or using small models for rapid tool extraction will be more convenient for external tool calls. The setting of the entire Agent should not be limited to specific things, but should be the entire pipeline that is continuously iterated to ultimately achieve a self-sufficient process from project deployment to launch. The project points out that large models use more detailed and more restrictive prompts, and the results obtained are very significant. For example, the ScreenToCode project, the core logic is to call the large model to perform image recognition output according to the specified prompts.

### Expected Architecture Design

![alt text](docs/image.png)

### Actual Output

| Project                                                | Description                                                                                                                                                                   |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [agent-fastpy](agent-fastpy)                           | A simple process management implemented with Python + Fastapi + React                                                                                                         |
| [agent_playground](agent_playground)                   | A pure command-line Agent with multi-task step flow implemented in Python                                                                                                     |
| [think-work](https://hub.oomol.com/package/think-work) | The entire process [oomol](https://oomol.com/zh-CN/) of the Agent is implemented using low-code for quickly writing the required front-end framework for a given requirement. |

## License

[GPL](LICENSE)
