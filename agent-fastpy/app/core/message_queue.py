from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from queue import Queue
from threading import Lock
from logger import Logger

@dataclass
class Message:
    """消息数据类"""
    topic: str
    content: Any
    sender: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class MessageQueue:
    """消息队列系统，用于管理智能体间的异步通信"""

    def __init__(self, name: str, max_size: int = 1000):
        self.name = name
        self.logger = Logger(f"queue_{name}")
        self.queues: Dict[str, Queue] = {}
        self.subscribers: Dict[str, List[Callable]] = {}
        self.max_size = max_size
        self.lock = Lock()

    def create_queue(self, topic: str) -> None:
        """创建新的消息队列"""
        with self.lock:
            if topic not in self.queues:
                self.queues[topic] = Queue(maxsize=self.max_size)
                self.subscribers[topic] = []
                self.logger.info(f"创建新队列: {topic}")

    def publish(self, message: Message) -> bool:
        """发布消息到指定主题"""
        try:
            if message.topic not in self.queues:
                self.create_queue(message.topic)

            queue = self.queues[message.topic]
            if queue.full():
                self.logger.warning(f"队列 {message.topic} 已满")
                return False

            queue.put(message)
            self.logger.info(
                f"消息已发布: {message.topic} - 来自 {message.sender}"
            )

            # 通知订阅者
            for callback in self.subscribers[message.topic]:
                try:
                    callback(message)
                except Exception as e:
                    self.logger.error(f"订阅者回调执行失败: {str(e)}")

            return True
        except Exception as e:
            self.logger.error(f"发布消息失败: {str(e)}")
            return False

    def subscribe(self, topic: str, callback: Callable[[Message], None]) -> None:
        """订阅指定主题"""
        with self.lock:
            if topic not in self.queues:
                self.create_queue(topic)
            self.subscribers[topic].append(callback)
            self.logger.info(f"新订阅者已添加到主题: {topic}")

    def unsubscribe(self, topic: str, callback: Callable[[Message], None]) -> None:
        """取消订阅"""
        with self.lock:
            if topic in self.subscribers and callback in self.subscribers[topic]:
                self.subscribers[topic].remove(callback)
                self.logger.info(f"订阅者已从主题移除: {topic}")

    def get_message(self, topic: str, timeout: Optional[float] = None) -> Optional[Message]:
        """从指定主题获取消息"""
        try:
            if topic not in self.queues:
                return None

            queue = self.queues[topic]
            message = queue.get(timeout=timeout) if timeout else queue.get_nowait()
            self.logger.debug(f"消息已获取: {topic}")
            return message
        except Exception as e:
            self.logger.debug(f"获取消息失败: {str(e)}")
            return None

    def get_queue_size(self, topic: str) -> int:
        """获取指定主题队列的当前大小"""
        return self.queues[topic].qsize() if topic in self.queues else 0

    def clear_queue(self, topic: str) -> None:
        """清空指定主题的队列"""
        with self.lock:
            if topic in self.queues:
                while not self.queues[topic].empty():
                    self.queues[topic].get_nowait()
                self.logger.info(f"队列已清空: {topic}")

    def list_topics(self) -> List[str]:
        """列出所有可用的主题"""
        return list(self.queues.keys())

    def get_subscriber_count(self, topic: str) -> int:
        """获取指定主题的订阅者数量"""
        return len(self.subscribers[topic]) if topic in self.subscribers else 0