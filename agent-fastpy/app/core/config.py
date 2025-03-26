import os
from dotenv import load_dotenv
from typing import Optional

class Config:
    def __init__(self):
        load_dotenv()
        self.dashscope_api_key: Optional[str] = os.getenv("DASHSCOPE_API_KEY")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.max_retries: int = int(os.getenv("MAX_RETRIES", "3"))

    def validate(self) -> bool:
        """验证必要配置是否已设置"""
        if not self.dashscope_api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
        return True

# 单例配置实例
config = Config()
