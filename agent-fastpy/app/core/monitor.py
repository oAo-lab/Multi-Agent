import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from app.core.logger import Logger

class TaskMonitor:
    """任务监控器，负责跟踪任务进度和存储中间产物"""
    
    def __init__(self, output_dir: str = "monitor_output"):
        self.logger = Logger("TaskMonitor")
        self.output_dir = Path(output_dir)
        self.current_task: Optional[Dict] = None
        self.task_history: List[Dict] = []
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"任务监控器初始化完成，输出目录：{self.output_dir}")

    def initialize_task(self, task_id: str, task_name: str, description: str) -> None:
        """初始化任务上下文"""
        self.current_task = {
            "id": task_id,
            "name": task_name,
            "description": description,
            "start_time": datetime.now().isoformat(),
            "status": "initializing",
            "artifacts": [],
            "logs": [],
            "agent_messages": {},  # 存储智能体之间的消息
            "agent_states": {}     # 存储智能体状态
        }
        self.task_history.append(self.current_task)
        self.logger.info(f"初始化任务：{task_name} (ID: {task_id})")

    def register_agent(self, task_id: str, agent_name: str, role: str) -> None:
        """注册智能体到任务"""
        if not self.current_task or self.current_task["id"] != task_id:
            raise ValueError(f"任务 {task_id} 未初始化")
            
        self.current_task["agent_states"][agent_name] = {
            "role": role,
            "status": "ready",
            "last_update": datetime.now().isoformat()
        }
        self.current_task["agent_messages"][agent_name] = []
        self.logger.info(f"注册智能体到任务：{agent_name} ({role})")

    def add_agent_message(self, task_id: str, sender: str, receiver: str, message: str) -> None:
        """添加智能体之间的消息"""
        if not self.current_task or self.current_task["id"] != task_id:
            raise ValueError(f"任务 {task_id} 未初始化")
            
        if sender not in self.current_task["agent_states"]:
            raise ValueError(f"发送者 {sender} 未注册")
            
        if receiver not in self.current_task["agent_states"]:
            raise ValueError(f"接收者 {receiver} 未注册")
            
        message_data = {
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        self.current_task["agent_messages"][receiver].append(message_data)
        self.logger.debug(f"添加消息：{sender} -> {receiver}")

    def get_agent_messages(self, task_id: str, agent_name: str) -> List[Dict]:
        """获取指定智能体的消息"""
        if not self.current_task or self.current_task["id"] != task_id:
            raise ValueError(f"任务 {task_id} 未初始化")
            
        if agent_name not in self.current_task["agent_states"]:
            raise ValueError(f"智能体 {agent_name} 未注册")
            
        return self.current_task["agent_messages"].get(agent_name, [])

    def update_agent_status(self, task_id: str, agent_name: str, status: str) -> None:
        """更新智能体状态"""
        if not self.current_task or self.current_task["id"] != task_id:
            raise ValueError(f"任务 {task_id} 未初始化")
            
        if agent_name not in self.current_task["agent_states"]:
            raise ValueError(f"智能体 {agent_name} 未注册")
            
        self.current_task["agent_states"][agent_name]["status"] = status
        self.current_task["agent_states"][agent_name]["last_update"] = datetime.now().isoformat()
        self.logger.debug(f"更新智能体状态：{agent_name} -> {status}")


    def start_task(self, task_name: str, description: str) -> str:
        """开始一个新任务"""
        task_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.current_task = {
            "id": task_id,
            "name": task_name,
            "description": description,
            "start_time": datetime.now().isoformat(),
            "status": "running",
            "artifacts": [],
            "logs": []
        }
        self.task_history.append(self.current_task)
        self.logger.info(f"开始任务：{task_name} (ID: {task_id})")
        return task_id

    def add_artifact(self, artifact_type: str, content: str, metadata: Optional[Dict] = None) -> None:
        """添加任务产物"""
        if not self.current_task:
            raise ValueError("没有正在进行的任务")

        artifact_id = f"artifact_{len(self.current_task['artifacts']) + 1}"
        artifact_file = self.output_dir / f"{self.current_task['id']}_{artifact_id}.md"
        
        # 创建Markdown文件
        with open(artifact_file, "w", encoding="utf-8") as f:
            f.write(content)

        artifact_info = {
            "id": artifact_id,
            "type": artifact_type,
            "file_path": str(artifact_file),
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        self.current_task["artifacts"].append(artifact_info)
        self.logger.debug(f"添加产物：{artifact_type} ({artifact_id})")

    def log_event(self, event_type: str, message: str) -> None:
        """记录任务事件"""
        if not self.current_task:
            raise ValueError("没有正在进行的任务")

        event = {
            "type": event_type,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.current_task["logs"].append(event)
        self.logger.debug(f"记录事件：{event_type} - {message}")

    def end_task(self, status: str = "completed") -> None:
        """结束当前任务"""
        if not self.current_task:
            raise ValueError("没有正在进行的任务")

        self.current_task["end_time"] = datetime.now().isoformat()
        self.current_task["status"] = status
        
        # 保存任务报告
        report_file = self.output_dir / f"{self.current_task['id']}_report.md"
        self._generate_report(report_file)
        
        self.logger.info(f"结束任务：{self.current_task['name']} (状态：{status})")
        self.current_task = None

    def _generate_report(self, file_path: Path) -> None:
        """生成Markdown格式的任务报告"""
        if not self.current_task:
            return

        with open(file_path, "w", encoding="utf-8") as f:
            # 任务基本信息
            f.write(f"# 任务报告：{self.current_task['name']}\n\n")
            f.write(f"- **任务ID**: {self.current_task['id']}\n")
            f.write(f"- **描述**: {self.current_task['description']}\n")
            f.write(f"- **状态**: {self.current_task['status']}\n")
            f.write(f"- **开始时间**: {self.current_task['start_time']}\n")
            f.write(f"- **结束时间**: {self.current_task.get('end_time', '进行中')}\n\n")

            # 事件日志
            f.write("## 事件日志\n")
            for event in self.current_task['logs']:
                f.write(f"- **{event['type']}** ({event['timestamp']}): {event['message']}\n")
            f.write("\n")

            # 任务产物
            f.write("## 任务产物\n")
            for artifact in self.current_task['artifacts']:
                f.write(f"### {artifact['type']} ({artifact['id']})\n")
                f.write(f"- **文件路径**: {artifact['file_path']}\n")
                f.write(f"- **时间戳**: {artifact['timestamp']}\n")
                if artifact['metadata']:
                    f.write("- **元数据**:\n")
                    for k, v in artifact['metadata'].items():
                        f.write(f"  - {k}: {v}\n")
                f.write("\n")

    def get_task_summary(self) -> List[Dict]:
        """获取所有任务的摘要信息"""
        return [{
            "id": task["id"],
            "name": task["name"],
            "status": task["status"],
            "start_time": task["start_time"],
            "end_time": task.get("end_time")
        } for task in self.task_history]

# 单例监控器实例
monitor = TaskMonitor()
