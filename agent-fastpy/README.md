# 智能体乐园

这是一个基于通义API的智能体交互系统，允许多个智能体在环境中相互交流和协作。

## 功能特点

- 支持多个智能体同时存在和交互
- 基于通义API进行智能对话
- 可扩展的智能体角色系统
- 完整的交互历史记录
- 智能体记忆功能

## 环境要求

- Python 3.7+
- 通义API密钥（DASHSCOPE_API_KEY）

## 安装

1. 克隆项目到本地
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 创建`.env`文件并设置API密钥：
   ```
   DASHSCOPE_API_KEY=your_api_key_here
   ```

## 使用方法

1. 运行主程序：
   ```bash
   python main.py
   ```

2. 示例代码展示了如何创建智能体并进行交互：
   - 创建教师、学生和助教角色
   - 模拟学生提问场景
   - 查看交互历史

## 扩展开发

你可以通过继承`BaseAgent`类来创建新的智能体类型，或者通过修改`Environment`类来增加新的交互方式。

---

```cmd
uvicorn app.main:app --reload --port 8000
```