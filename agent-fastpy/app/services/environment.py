from typing import Optional
from environment import Environment

_environment: Optional[Environment] = None

def get_environment() -> Environment:
    """获取全局Environment实例"""
    global _environment
    if _environment is None:
        _environment = Environment()
    return _environment

def set_environment(env: Environment) -> None:
    """设置全局Environment实例"""
    global _environment
    _environment = env