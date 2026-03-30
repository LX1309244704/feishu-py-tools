"""
Schema模块
"""
import json
from pathlib import Path
from typing import Dict, Any

SCHEMA_DIR = Path(__file__).parent.parent / "schemas"


def get_schema(schema_name: str) -> Dict[str, Any]:
    """
    获取Schema
    
    Args:
        schema_name: Schema名称（不带.json后缀）
        
    Returns:
        Schema字典
    """
    schema_path = SCHEMA_DIR / f"{schema_name}.json"
    if not schema_path.exists():
        raise ValueError(f"Schema不存在: {schema_name}")
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


__all__ = ['get_schema']
