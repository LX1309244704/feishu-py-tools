"""
配置管理模块
支持GUI配置持久化存储
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置目录，默认~/.weiyuan
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / '.weiyuan'
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / 'config.json'
        
        # 默认配置
        self._default_config = {
            # 飞书配置
            'feishu': {
                'app_id': '',
                'app_secret': '',
            },
            # 企业微信配置
            'wechat_work': {
                'corp_id': '',
                'corp_secret': '',
                'agent_id': '',
                'external_contact_secret': '',  # 客户联系专用
            },
            # 公众号配置
            'wechat_mp': {
                'app_id': '',
                'app_secret': '',
            },
            # AI配置
            'ai': {
                'openai_api_key': '',
                'openai_base_url': 'https://api.openai.com/v1',
                'anthropic_api_key': '',
                'dashscope_api_key': '',  # 通义千问
            },
            # 通用配置
            'general': {
                'default_flow_dir': str(Path.home() / 'weiyuan_flows'),
                'log_dir': str(self.config_dir / 'logs'),
                'theme': 'light',
                'language': 'zh_CN',
            }
        }
        
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置（处理新增字段）
                return self._merge_config(self._default_config, config)
            except Exception as e:
                print(f"加载配置失败：{e}，使用默认配置")
                return self._default_config.copy()
        return self._default_config.copy()
    
    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """合并配置，保留用户设置同时添加新增字段"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key].update(value)
            else:
                result[key] = value
        return result
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置失败：{e}")
            return False
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self._config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any):
        """设置配置值"""
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """获取整个配置段"""
        return self._config.get(section, {}).copy()
    
    def set_section(self, section: str, values: Dict[str, Any]):
        """设置整个配置段"""
        self._config[section] = values
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()
    
    def reset_to_default(self):
        """重置为默认配置"""
        self._config = self._default_config.copy()
        self.save_config()


# 全局配置实例
_config_instance = None

def get_config() -> ConfigManager:
    """获取全局配置实例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance
