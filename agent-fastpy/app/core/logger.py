import logging
import os
import sys
import threading
from logging.handlers import RotatingFileHandler
from typing import Optional, Callable, Any
from functools import wraps

class Logger:
    """日志管理器，负责配置和管理日志系统"""

    _lock = threading.Lock()
    
    def __init__(self, name: str, log_dir: str = "logs", max_size: int = 10 * 1024 * 1024, backup_count: int = 5):
        self.name = name
        self.log_dir = log_dir
        self.max_size = max_size  # 单个日志文件最大大小，默认10MB
        self.backup_count = backup_count  # 保留的日志文件数量
        self.logger: Optional[logging.Logger] = None
        self._setup_logger()

    def _setup_logger(self) -> None:
        """配置日志记录器"""
        with Logger._lock:
            # 创建日志目录
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

            # 配置日志记录器
            self.logger = logging.getLogger(self.name)
            self.logger.setLevel(logging.DEBUG)

            # 创建轮转文件处理器
            file_handler = RotatingFileHandler(
                os.path.join(self.log_dir, f"{self.name}.log"),
                maxBytes=self.max_size,
                backupCount=self.backup_count,
                encoding="utf-8"
            )
            file_handler.setLevel(logging.DEBUG)

            # 创建控制台处理器
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)

            # 设置更丰富的日志格式
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # 清除旧处理器
            self.logger.handlers.clear()

            # 添加处理器
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def set_level(self, level: str) -> None:
        """动态设置日志级别"""
        log_level = getattr(logging, level.upper(), None)
        if isinstance(log_level, int):
            self.logger.setLevel(log_level)
            for handler in self.logger.handlers:
                handler.setLevel(log_level)

    @staticmethod
    def catch_exceptions(logger: logging.Logger):
        """捕获异常的装饰器"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception(f"捕获到异常：{str(e)}")
                    raise
            return wrapper
        return decorator

    def debug(self, message: str) -> None:
        """记录调试信息"""
        if self.logger:
            self.logger.debug(message)

    def info(self, message: str) -> None:
        """记录一般信息"""
        if self.logger:
            self.logger.info(message)

    def warning(self, message: str) -> None:
        """记录警告信息"""
        if self.logger:
            self.logger.warning(message)

    def error(self, message: str) -> None:
        """记录错误信息"""
        if self.logger:
            self.logger.error(message)

    def critical(self, message: str) -> None:
        """记录严重错误信息"""
        if self.logger:
            self.logger.critical(message)
