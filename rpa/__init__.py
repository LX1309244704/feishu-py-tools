"""
RPA机器人流程自动化工具
基于opencli/飞书Python工具箱的自动化工作流引擎

核心功能：
- YAML/JSON格式流程定义，低代码开发
- 丰富的插件生态（飞书、数据处理、文件操作、HTTP等）
- 多维度触发（定时、Webhook、事件、手动）
- 变量系统、上下文传递、表达式支持
- 错误重试、超时控制、失败回调
- CLI命令行工具

使用示例：
```bash
# 创建新流程
opencli rpa init 库存预警流程

# 验证流程格式
opencli rpa validate inventory_alert.yaml

# 执行流程
opencli rpa run inventory_alert.yaml

# 列出所有流程
opencli rpa list

# 查看已安装插件
opencli rpa plugin list
```
"""

# 导入核心模块
from rpa.core.flow import Flow, load_flow
from rpa.core.engine import ExecutionEngine, execution_engine
from rpa.core.plugin import BasePlugin, register_plugin, get_plugin, list_plugins
from rpa.core.variable_engine import VariableEngine, variable_engine

# 版本
__version__ = "1.0.0"

__all__ = [
    'Flow',
    'load_flow',
    'ExecutionEngine',
    'execution_engine',
    'BasePlugin',
    'register_plugin',
    'get_plugin',
    'list_plugins',
    'VariableEngine',
    'variable_engine',
]
