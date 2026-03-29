"""
插件系统
"""
from typing import Dict, Any, List, Optional, Callable
from abc import ABC, abstractmethod
from pathlib import Path
import json
import yaml
from datetime import datetime


class Plugin(ABC):
    """插件基类"""
    
    def __init__(self, plugin_id: str, name: str, version: str = "1.0",
                 description: str = "", author: str = ""):
        """
        初始化插件
        
        Args:
            plugin_id: 插件ID
            name: 插件名称
            version: 版本号
            description: 描述
            author: 作者
        """
        self.plugin_id = plugin_id
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.enabled = True
        self.config = {}
        self.hooks = {}
        self.dependencies = []
        self.metadata = {}
        self.install_path = Path.home() / ".feishu-py-tools/plugins" / f"{plugin_id}.json"
        
        self._load_metadata()
    
    @abstractmethod
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行插件功能（抽象方法）
        
        Args:
            params: 参数字典
            context: 上下文数据
            
        Returns:
            执行结果
        """
        raise NotImplementedError("execute方法必须由子类实现")
    
    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """
        获取配置schema（抽象方法）
        
        Returns:
            配置schema
        """
        raise NotImplementedError("get_config_schema方法必须由子类实现")
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取插件信息
        
        Returns:
            插件信息字典
        """
        return {
            "plugin_id": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "enabled": self.enabled,
            "dependencies": self.dependencies,
            "hooks": list(self.hooks.keys())
        }
    
    def _load_metadata(self):
        """加载元数据"""
        if self.install_path.exists():
            with open(self.install_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                self.config = metadata.get("config", {})
                self.hooks = metadata.get("hooks", {})
                self.dependencies = metadata.get("dependencies", [])
                self.metadata = metadata
                print(f"加载插件: {self.name}")
    
    def _save_metadata(self):
        """保存元数据"""
        metadata = {
            "id": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "config": self.config,
            "hooks": self.hooks,
            "dependencies": self.dependencies,
            "metadata": self.metadata
        }
        
        self.install_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.install_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def add_hook(self, hook_name: str, hook_func: Callable):
        """
        添加钩子函数
        
        Args:
            hook_name: 钩子名称
            hook_func: 钩子函数
        """
        self.hooks[hook_name] = hook_func
        self._save_metadata()
    
    def enable(self):
        """启用插件"""
        self.enabled = True
        self._save_metadata()
    
    def disable(self):
        """禁用插件"""
        self.enabled = False
        self._save_metadata()
    
    def update_config(self, config: Dict[str, Any]):
        """
        更新配置
        
        Args:
            config: 新的配置
        """
        self.config.update(config)
        self._save_metadata()
    
    def validate_config(self) -> bool:
        """
        验证配置是否有效
        
        Returns:
            是否有效
        """
        schema = self.get_config_schema()
        for key, field in schema.get("required", {}).items():
            if key not in self.config:
                print(f"缺少必需配置项: {key}")
                return False
            
        return True
    
    def __repr__(self):
        return f"Plugin({self.plugin_id}): {self.name} v{self.version}"


class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugins_dir: str = None):
        """
        初始化插件管理器
        
        Args:
            plugins_dir: 插件目录
        """
        self.plugins_dir = Path(plugins_dir) or Path.home() / ".feishu-py-tools/plugins"
        self.plugins_dir = self.plugins_dir
        self.plugins = {}
        self.plugins_cache = {}
        self.plugin_types = {
            "bitable": "多维表格",
            "doc": "文档",
            "calendar": "日历",
            "task": "任务",
            "message": "消息",
            "notification": "通知",
            "data_processing": "数据处理",
            "visualization": "数据可视化",
            "workflow": "工作流"
        }
    
    def load_plugins(self):
        """加载所有插件"""
        if not self.plugins_dir.exists():
            print("插件目录不存在，创建中...")
            self.plugins_dir.mkdir(parents=True, exist_ok=True)
            return
        
        for plugin_file in self.plugins_dir.glob("*.json"):
            try:
                with open(plugin_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    self.plugins_cache[metadata['id']] = Plugin(
                        plugin_id=metadata['id'],
                        name=metadata['name'],
                        version=metadata['version'],
                        description=metadata['description'],
                        author=metadata['author']
                    )
                    
                    # 加载配置
                    if 'config' in metadata:
                        self.plugins_cache[metadata['id']].config = metadata['config']
                    
                    # 加载钩子
                    if 'hooks' in metadata:
                        for hook_name, hook_info in metadata['hooks'].items():
                            self.plugins_cache[metadata['id']].add_hook(hook_name, hook_info)
                    
                    # 加载依赖
                    if 'dependencies' in metadata:
                        self.plugins_cache[metadata['id']].dependencies = metadata['dependencies']
                    
                    print(f"加载插件: {metadata['name']} v{metadata['version']}")
            except Exception as e:
                print(f"加载插件失败 {plugin_file}: {e}")
        
        print(f"加载了 {len(self.plugins_cache)} 个插件")
    
    def register_plugin(self, plugin: Plugin):
        """
        注册插件

        Args:
            plugin: 插件对象
        """
        self.plugins[plugin.plugin_id] = plugin
        self.plugins_cache[plugin.plugin_id] = plugin
        self._save_plugin_file(plugin)
        print(f"注册插件: {plugin.name}")
    
    def _save_plugin_file(self, plugin: Plugin):
        """保存插件文件"""
        metadata = {
            "id": plugin.plugin_id,
            "name": plugin.name,
            "version": plugin.version,
            "description": plugin.description,
            "author": plugin.author,
            "config": plugin.config,
            "hooks": plugin.hooks,
            "dependencies": plugin.dependencies,
            "metadata": plugin.metadata
        }
        
        plugin_file = self.plugins_dir / f"{plugin.plugin_id}.json"
        plugin_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(plugin_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """
        获取插件
        
        """
        return self.plugins_cache.get(plugin_id)
    
    def list_plugins(self, plugin_type: str = None) -> List[Plugin]:
        """
        列出插件
        
        Args:
            plugin_type: 插件类型
            
        Returns:
            插件列表
        """
        plugins = list(self.plugins_cache.values())

        if plugin_type and plugin_type in self.plugin_types:
            return [p for p in plugins if p.metadata.get("type") == plugin_type]

        return plugins
    
    def get_enabled_plugins(self) -> List[Plugin]:
        """获取已启用的插件"""
        return [p for p in self.plugins_cache.values() if p.enabled]
    
    def get_plugins_by_type(self, plugin_type: str) -> List[Plugin]:
        """获取指定类型的插件"""
        return [p for p in self.plugins_cache.values() if p.metadata.get("type") == plugin_type]
    
    def enable_plugin(self, plugin_id: str) -> bool:
        """启用插件"""
        plugin = self.get_plugin(plugin_id)
        if plugin:
            plugin.enable()
            self._save_plugin_file(plugin)
            print(f"插件 {plugin_id} 已启用")
            return True
        return False
    
    def disable_plugin(self, plugin_id: str) -> bool:
        """禁用插件"""
        plugin = self.get_plugin(plugin_id)
        if plugin:
            plugin.disable()
            self._save_plugin_file(plugin)
            print(f"插件 {plugin_id} 已禁用")
            return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_plugins": len(self.plugins_cache),
            "enabled_plugins": len(self.get_enabled_plugins()),
            "disabled_plugins": len([p for p in self.plugins_cache.values() if not p.enabled]),
            "total_dependencies": sum(len(p.dependencies) for p in self.plugins_cache.values()),
            "total_hooks": sum(len(p.hooks) for p in self.plugins_cache.values()),
            "plugin_types": list(set([p.metadata.get("type", "unknown") for p in self.plugins_cache.values()]))
        }
    
    def export_plugins(self, filename: str = "plugins.json") -> str:
        """导出插件列表"""
        export_data = [
            {
                "id": p.plugin_id,
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "author": p.author,
                "enabled": p.enabled
            }
            for p in self.plugins_cache.values()
        ]
        
        export_file = self.plugins_dir / filename
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return str(export_file)
    
    def get_all_plugins_info(self) -> List[Dict[str, Any]]:
        """
        获取所有插件的完整信息
        
        Returns:
            插件信息列表
        """
        return [
            {
                **p.get_info(),
                "config": p.config,
                "dependencies": p.dependencies,
                "hooks": list(p.hooks.keys())
            }
            for p in self.plugins_cache.values()
        ]
