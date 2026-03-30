"""
RPA流程模型
"""
import yaml
import json
import jsonschema
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from rpa.schemas import get_schema


class Flow:
    """RPA流程类"""
    
    def __init__(self, flow_path: str):
        """
        初始化流程
        
        Args:
            flow_path: 流程文件路径（YAML/JSON格式）
        """
        self.flow_path = Path(flow_path)
        self.raw_data = self._load_file()
        self.schema = get_schema("flow_schema")
        self._validate()
        self._parse()
    
    def _load_file(self) -> Dict[str, Any]:
        """加载流程文件"""
        if not self.flow_path.exists():
            raise FileNotFoundError(f"流程文件不存在: {self.flow_path}")
        
        suffix = self.flow_path.suffix.lower()
        if suffix in ['.yaml', '.yml']:
            with open(self.flow_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        elif suffix == '.json':
            with open(self.flow_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise ValueError(f"不支持的文件格式: {suffix}，仅支持YAML/JSON")
    
    def _validate(self):
        """验证流程格式合法性"""
        try:
            jsonschema.validate(instance=self.raw_data, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"流程格式错误: {e.message}")
    
    def _parse(self):
        """解析流程数据"""
        self.name = self.raw_data['name']
        self.description = self.raw_data.get('description', '')
        self.version = self.raw_data.get('version', '1.0.0')
        self.trigger = self.raw_data.get('trigger', {'type': 'manual'})
        self.variables = self.raw_data.get('variables', {})
        self.steps = self.raw_data['steps']
        self.on_success = self.raw_data.get('on_success', [])
        self.on_failure = self.raw_data.get('on_failure', [])
        self.settings = self.raw_data.get('settings', {})
        
        # 解析设置
        self.max_parallel = self.settings.get('max_parallel', 1)
        self.log_level = self.settings.get('log_level', 'info')
        self.timeout = self.settings.get('timeout', 3600)
        
        # 元数据
        self.created_at = datetime.now()
        self.last_modified = datetime.fromtimestamp(self.flow_path.stat().st_mtime)
    
    def get_step_by_name(self, step_name: str) -> Optional[Dict[str, Any]]:
        """根据步骤名称获取步骤配置"""
        for step in self.steps:
            if step['name'] == step_name:
                return step
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'trigger': self.trigger,
            'variables': self.variables,
            'steps_count': len(self.steps),
            'settings': self.settings,
            'created_at': self.created_at.isoformat(),
            'last_modified': self.last_modified.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"Flow(name='{self.name}', version='{self.version}', steps={len(self.steps)})"


def load_flow(flow_path: str) -> Flow:
    """加载流程文件"""
    return Flow(flow_path)
