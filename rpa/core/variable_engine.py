"""
变量解析引擎
"""
import re
from typing import Dict, Any, Optional
from datetime import datetime, date
import jinja2
from jinja2 import Template, meta


class VariableEngine:
    """变量解析引擎"""
    
    # 变量匹配正则：${{ variable }}
    VAR_PATTERN = re.compile(r'\$\{\{([^}]+)\}\}')
    
    def __init__(self):
        """初始化变量引擎"""
        self.env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=False
        )
        
        # 注册内置函数
        self._register_builtins()
    
    def _register_builtins(self):
        """注册内置函数"""
        self.env.globals.update({
            'now': datetime.now,
            'today': date.today,
            'datetime': datetime,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'len': len,
            'sum': sum,
            'max': max,
            'min': min,
            'upper': lambda s: s.upper() if isinstance(s, str) else s,
            'lower': lambda s: s.lower() if isinstance(s, str) else s,
            'format_date': lambda dt, fmt='%Y-%m-%d': dt.strftime(fmt) if isinstance(dt, (datetime, date)) else str(dt),
            'json_dumps': json.dumps,
            'json_loads': json.loads
        })
    
    def render(self, template: Any, context: Dict[str, Any]) -> Any:
        """
        渲染模板，替换变量
        
        Args:
            template: 模板内容，可以是字符串、字典、列表
            context: 上下文数据
            
        Returns:
            渲染后的结果
        """
        if isinstance(template, str):
            return self._render_string(template, context)
        elif isinstance(template, dict):
            return {k: self.render(v, context) for k, v in template.items()}
        elif isinstance(template, list):
            return [self.render(item, context) for item in template]
        else:
            return template
    
    def _render_string(self, template_str: str, context: Dict[str, Any]) -> Any:
        """渲染字符串模板"""
        # 先判断是否包含变量
        if not self.VAR_PATTERN.search(template_str):
            return template_str
        
        try:
            template = self.env.from_string(template_str)
            result = template.render(**context)
            
            # 尝试转换为原始类型
            try:
                return json.loads(result)
            except (json.JSONDecodeError, ValueError):
                return result
                
        except Exception as e:
            raise ValueError(f"变量渲染失败: {str(e)}，模板: {template_str}")
    
    def evaluate_expression(self, expression: str, context: Dict[str, Any]) -> bool:
        """
        计算条件表达式结果
        
        Args:
            expression: 条件表达式（比如len(steps.获取数据.output) > 0）
            context: 上下文数据
            
        Returns:
            布尔值结果
        """
        try:
            template = self.env.from_string(f"{{% if {expression} %}}True{{% else %}}False{{% endif %}}")
            result = template.render(**context)
            return result == 'True'
        except Exception as e:
            raise ValueError(f"表达式计算失败: {str(e)}，表达式: {expression}")
    
    def extract_variables(self, template_str: str) -> List[str]:
        """提取模板中使用的所有变量"""
        ast = self.env.parse(template_str)
        return list(meta.find_undeclared_variables(ast))
    
    def merge_context(self, *contexts: Dict[str, Any]) -> Dict[str, Any]:
        """合并多个上下文"""
        merged = {}
        for ctx in contexts:
            merged.update(ctx)
        return merged


# 全局变量引擎实例
variable_engine = VariableEngine()

__all__ = ['VariableEngine', 'variable_engine']
