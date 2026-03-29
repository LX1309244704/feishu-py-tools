"""
配置管理模块
"""
import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，默认为 ~/.feishu-py-tools/config.yaml
        """
        if config_path is None:
            config_path = os.path.expanduser("~/.feishu-py-tools/config.yaml")
        
        self.config_path = Path(config_path)
        self.config_dir = self.config_path.parent
        self.config: Dict[str, Any] = {}
        
        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def init_config(self):
        """初始化配置文件"""
        if self.config_path.exists():
            print(f"配置文件已存在: {self.config_path}")
            return
        
        default_config = {
            "feishu": {
                "app_id": "",
                "app_secret": "",
                "encrypt_key": "",
                "verification_token": ""
            },
            "ai": {
                "claude": {
                    "api_key": "",
                    "model": "claude-3-5-sonnet-20241022"
                },
                "openai": {
                    "api_key": "",
                    "model": "gpt-4o"
                },
                "deepseek": {
                    "api_key": "",
                    "model": "deepseek-chat"
                }
            },
            "database": {
                "type": "sqlite",
                "path": "~/.feishu-py-tools/data.db"
            },
            "logging": {
                "level": "INFO",
                "file": "~/.feishu-py-tools/logs/feishu-py-tools.log",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "templates": {
                "path": "~/.feishu-py-tools/templates"
            }
        }
        
        # 保存配置
        self.save_config(default_config)
        print(f"配置文件已创建: {self.config_path}")
        print("请编辑配置文件，填入你的飞书应用凭据")
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            print(f"配置文件不存在: {self.config_path}")
            print("请运行: feishu-cli config init")
            return {}
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        return self.config
    
    def save_config(self, config: Dict[str, Any]):
        """保存配置文件"""
        self.config = config
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键，支持点分隔的嵌套键，如 'feishu.app_id'
            default: 默认值
            
        Returns:
            配置值
        """
        if not self.config:
            self.load_config()
        
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        设置配置项
        
        Args:
            key: 配置键，支持点分隔的嵌套键，如 'feishu.app_id'
            value: 配置值
        """
        if not self.config:
            self.load_config()
        
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config(self.config)
    
    def get_auth_url(self) -> str:
        """获取飞书应用授权URL"""
        app_id = self.get("feishu.app_id")
        if not app_id:
            raise ValueError("请先配置 feishu.app_id")
        
        redirect_uri = "https://open.feishu.cn/common/unify/api/oidc/redirect"
        return f"https://open.feishu.cn/open-apis/authen/v1/authorize?app_id={app_id}&redirect_uri={redirect_uri}&scope=&state=STATE"
    
    def validate_config(self) -> bool:
        """验证配置是否完整"""
        required_keys = [
            "feishu.app_id",
            "feishu.app_secret"
        ]
        
        for key in required_keys:
            if not self.get(key):
                print(f"缺少必需配置: {key}")
                return False
        
        return True


def get_config() -> ConfigManager:
    """获取全局配置管理器"""
    return ConfigManager()
