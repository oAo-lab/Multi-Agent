import logging
from typing import Any, Dict, Optional

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("agent_playground.log"),  # 记录到文件
        logging.StreamHandler(),  # 在终端输出
    ],
)

logger = logging.getLogger(__name__)


def log_event(event_type: str, message: str, data: Optional[Dict[str, Any]] = None):
    """记录日志事件"""
    log_message = f"[{event_type}] {message}"
    if data:
        log_message += f" | 详情: {data}"

    logger.info(log_message)
