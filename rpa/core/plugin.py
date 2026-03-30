"""
RPA插件基类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime


class BasePlugin(ABC):
    """插件基类"""
    
    # 插件元数据，子类必须实现
    plugin_name: str = ""
    plugin_version: str = "1.0.0"
    plugin_description: str = ""
    plugin_author: str = ""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化插件
        
        Args:
            config: 插件全局配置
        """
        self.config = config or {}
        self.logger = None
        self.context = {}
    
    @abstractmethod
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行插件动作（必须由子类实现）
        
        Args:
            params: 步骤传入的参数
            context: 流程上下文
            
        Returns:
            执行结果字典，必须包含success字段
        """
        raise NotImplementedError("execute方法必须由子类实现")
    
    def get_params_schema(self) -> Dict[str, Any]:
        """
        获取参数Schema（可选实现），用于参数校验
        
        Returns:
            JSON Schema格式的参数定义
        """
        return {}
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        验证参数合法性（可选实现）
        
        Args:
            params: 待验证的参数
            
        Returns:
            是否合法，不合法时抛出异常
        """
        return True
    
    def log(self, level: str, message: str):
        """记录日志"""
        if self.logger:
            log_method = getattr(self.logger, level.lower(), self.logger.info)
            log_method(f"[{self.plugin_name}] {message}")
    
    def to_dict(self) -> Dict[str, Any]:
        """获取插件信息"""
        return {
            "name": self.plugin_name,
            "version": self.plugin_version,
            "description": self.plugin_description,
            "author": self.plugin_author
        }
    
    def __repr__(self) -> str:
        return f"Plugin({self.plugin_name}@{self.plugin_version})"


# 插件注册表
_plugin_registry: Dict[str, BasePlugin] = {}


def register_plugin(plugin_class: type[BasePlugin]) -> type[BasePlugin]:
    """
    注册插件装饰器
    
    Args:
        plugin_class: 插件类
        
    Returns:
        插件类
    """
    if not issubclass(plugin_class, BasePlugin):
        raise ValueError(f"插件必须继承自BasePlugin: {plugin_class}")
    
    plugin_key = f"{plugin_class.plugin_name}@{plugin_class.plugin_version}"
    _plugin_registry[plugin_key] = plugin_class
    
    # 同时注册不带版本的别名，方便使用
    _plugin_registry[plugin_class.plugin_name] = plugin_class
    
    return plugin_class


def get_plugin(plugin_ref: str) -> Optional[type[BasePlugin]]:
    """
    获取插件类
    
    Args:
        plugin_ref: 插件引用，格式：插件名@版本，或者插件名
        
    Returns:
        插件类，不存在返回None
    """
    if '@' in plugin_ref:
        name, version = plugin_ref.split('@', 1)
        key = f"{name}@{version}"
        return _plugin_registry.get(key) or _plugin_registry.get(name)
    else:
        return _plugin_registry.get(plugin_ref)


def list_plugins() -> List[Dict[str, Any]]:
    """获取所有已注册的插件列表"""
    plugins = []
    seen = set()
    
    for key, plugin_class in _plugin_registry.items():
        if '@' not in key:  # 只显示不带版本的
            plugins.append(plugin_class().to_dict())
    
    return plugins
