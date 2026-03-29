"""
工作流引擎
"""
import json
import asyncio
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum


class TriggerType(Enum):
    """触发器类型"""
    SCHEDULE = "schedule"      # 定时触发
    EVENT = "event"           # 事件触发
    CONDITION = "condition"    # 条件触发
    MANUAL = "manual"          # 手动触发
    API = "api"             # API触发


class OperatorType(Enum):
    """操作符类型"""
    EQUAL = "eq"           # 等于
    NOT_EQUAL = "ne"        # 不等于
    GREATER = "gt"         # 大于
    LESS = "lt"           # 小于
    GREATER_EQUAL = "ge"  # 大于等于
    LESS_EQUAL = "le"    # 小于等于
    CONTAINS = "in"        # 包含
    NOT_CONTAINS = "not_in"   # 不包含
    IS_NULL = "is_null"     # 为空
    NOT_NULL = "not_null"  # 不为空
    IS_TRUE = "is_true"    # 为真
    NOT_TRUE = "not_true"  # 不为真
    IN_LIST = "in_list"     # 在列表中


class StepType(Enum):
    """步骤类型"""
    API_CALL = "api_call"       # API调用
    CONDITION = "condition"     # 条件判断
    DATA_PROCESSING = "data_processing"  # 数据处理
    NOTIFICATION = "notification"  # 发送通知
    WORKFLOW = "workflow"      # 子工作流
    CODE = "code"              # 执行代码
    PLUGIN = "plugin"          # 插件调用


class Trigger:
    """触发器"""
    
    def __init__(self, trigger_id: str, trigger_type: TriggerType, 
                 config: Dict[str, Any] = None):
        """
        初始化触发器
        
        Args:
            trigger_id: 触发器ID
            trigger_type: 触发器类型
            config: 触发器配置
        """
        self.id = trigger_id
        self.type = trigger_type
        self.config = config or {}
        self.enabled = True
        self.last_triggered = None
        self.trigger_count = 0
        self.condition = None
    
    def check_condition(self, context: Dict[str, Any]) -> bool:
        """
        检查触发条件
        
        Args:
            context: 上下文数据
            
        Returns:
            是否触发
        """
        if not self.enabled:
            return False
        
        if self.condition is None:
            return True  # 没有条件，总是触发
        
        return self._evaluate_condition(self.condition, context)
    
    def _evaluate_condition(self, condition: Dict[str, Any], 
                         context: Dict[str, Any]) -> bool:
        """评估条件表达式"""
        try:
            left = self._get_value(condition.get("left"), context)
            right = self._get_value(condition.get("right"), context)
            operator = condition.get("operator")
            
            result = self._apply_operator(left, right, operator)
            return result
        except Exception as e:
            print(f"条件评估失败: {e}")
            return False
    
    def _get_value(self, path: str, context: Dict[str, Any]) -> Any:
        """获取值（支持嵌套路径）"""
        keys = path.split('.')
        value = context
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    def _apply_operator(self, left: Any, right: Any, operator: str) -> bool:
        """应用操作符"""
        operator_map = {
            OperatorType.EQUAL: lambda l, r: l == r,
            OperatorType.NOT_EQUAL: lambda l, r: l != r,
            OperatorType.GREATER: lambda l, r: l > r,
            OperatorType.LESS: lambda l, r: l < r,
            OperatorType.GREATER_EQUAL: lambda l, r: l >= r,
            OperatorType.LESS_EQUAL: lambda l, r: l <= r,
            OperatorType.CONTAINS: lambda l, r: l in r,
            OperatorType.NOT_CONTAINS: lambda l, r: l not in r,
            OperatorType.IS_NULL: lambda l, r: l is None,
            OperatorType.NOT_NULL: lambda l, r: l is not None,
            OperatorType.IS_TRUE: lambda l, r: l is True,
            OperatorType.NOT_TRUE: lambda l, r: l is not True,
            OperatorType.IN_LIST: lambda l, r: r in l if isinstance(r, list) else []
        }
        
        apply_func = operator_map.get(operator)
        if apply_func:
            return apply_func(left, right)
        
        return False
    
    def trigger(self, context: Dict[str, Any]) -> bool:
        """
        执行触发
        """
        self.last_triggered = datetime.now()
        self.trigger_count += 1
        
        print(f"触发器 {self.id} 被触发")
        return True
    
    def reset(self):
        """重置触发器"""
        self.last_triggered = None
        self.trigger_count = 0
    
    def disable(self):
        """禁用触发器"""
        self.enabled = False
    
    def enable(self):
        """启用触发器"""
        self.enabled = True


class Step:
    """工作流步骤"""
    
    def __init__(self, step_id: str, step_type: StepType, 
                 name: str, config: Dict[str, Any] = None):
        """
        初始化步骤
        
        Args:
            step_id: 步骤ID
            step_type: 步骤类型
            name: 步骤名称
            config: 步骤配置
        """
        self.id = step_id
        self.type = step_type
        self.name = name
        self.config = config or {}
        self.next_steps = []
        self.prev_steps = []
        self.parallel = False
        self.continue_on_failure = False
        retry_times = 3
    
    def execute(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行步骤
        
        Args:
            context: 上下文数据
            
        Returns:
            执行结果
        """
        if context is None:
            context = {}
        
        print(f"执行步骤: {self.name} (类型: {self.type})")
        
        try:
            if self.type == StepType.API_CALL:
                result = self._execute_api_call(context)
            elif self.type == StepType.CONDITION:
                result = self._execute_condition(context)
            elif self.type == StepType.DATA_PROCESSING:
                result = self._execute_data_processing(context)
            elif self.type == StepType.NOTIFICATION:
                result = self._execute_notification(context)
            elif self.type == StepType.WORKFLOW:
                result = self._execute_workflow(context)
            elif self.type == StepType.CODE:
                result = self._execute_code(context)
            elif self.type == StepType.PLUGIN:
                result = self._execute_plugin(context)
            else:
                print(f"未知步骤类型: {self.type}")
                result = {"success": False, "error": f"未知步骤类型: {self.type}"}
            
            print(f"步骤 {self.id} 执行完成")
            return result
            
        except Exception as e:
            print(f"步骤 {self.id} 执行失败: {e}")
            
            if not self.continue_on_failure:
                return {"success": False, "error": str(e)}
            
            # 重试机制
            self.retry_times -= 1
            if self.retry_times > 0:
                print(f"重试步骤 {self.id}，剩余 {self.retry_times} 次")
                return self.execute(context)
            
            return {"success": False, "error": str(e)}
    
    def _execute_api_call(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行API调用"""
        api_config = self.config.get("api")
        api_endpoint = api_config.get("endpoint")
        method = api_config.get("method", "GET")
        params = api_config.get("params", {})
        
        print(f"调用API: {method} {api_endpoint}")
        print(f"参数: {params}")
        
        # 这里应该实际调用API
        # 返回示例数据
        return {
            "success": True,
            "api_endpoint": api_endpoint,
            "method": method,
            "params": params,
            "result": "模拟API调用成功"
        }
    
    def _execute_condition(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行条件判断"""
        condition = self.config.get("condition")
        result = self._evaluate_condition(condition, context)
        
        return {
            "success": True,
            "condition": condition,
            "result": result
        }
    
    def _execute_data_processing(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行数据处理"""
        operation = self.config.get("operation")
        params = self.config.get("params", {})
        source_field = self.config.get("source_field")
        target_field = self.config.get("target_field")
        
        data = context.get("data", [])
        
        print(f"数据处理: {operation}")
        
        result = data
        if operation == "filter":
            field = params.get("field")
            value = params.get("value")
            result = [item for item in data if item.get(field) == value]
        elif operation == "sort":
            field = params.get("field")
            ascending = params.get("ascending", True)
            result = sorted(data, key=lambda x: x.get(field, ""), reverse=not ascending)
        elif operation == "aggregate":
            field = params.get("field")
            func = params.get("function")
            values = [item.get(field) for item in data if item.get(field)]
            
            if func == "sum":
                result = sum(values)
            elif func == "avg":
                result = sum(values) / len(values) if values else 0
            elif func == "max":
                result = max(values) if values else None
            elif func == "min":
                result = min(values) if values else None
            elif func == "count":
                result = len(values)
            elif func == "count_unique":
                result = len(set(values))
        
        return {
            "success": True,
            "operation": operation,
            "result": result
        }
    
    def _execute_notification(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """发送通知"""
        notification_config = self.config.get("notification")
        message = notification_config.get("message", "任务通知")
        recipient = notification_config.get("recipient", "ou_xxx")
        
        print(f"发送通知给 {recipient}: {message}")
        
        return {
            "success": True,
            "recipient": recipient,
            "message": message,
            "sent": True
        }
    
    def _execute_workflow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行子工作流"""
        workflow_id = self.config.get("workflow_id")
        sub_workflow = self.config.get("sub_workflow", {})
        
        print(f"执行子工作流: {workflow_id}")
        
        # 这里应该递归执行子工作流
        return {
            "success": True,
            "workflow_id": workflow_id,
            "sub_workflow": sub_workflow
        }
    
    def _execute_code(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行代码"""
        code = self.config.get("code", "")
        
        print(f"执行代码: {code}")
        
        # 这里应该安全地执行代码
        return {
            "success": True,
            "code_executed": True
        }
    
    def _execute_plugin(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行插件调用"""
        plugin_id = self.config.get("plugin_id")
        plugin_action = self.config.get("action", "")
        params = self.config.get("params", {})
        
        print(f"调用插件: {plugin_id} / {plugin_action}")
        
        # 这里应该实际调用插件
        return {
            "success": True,
            "plugin_id": plugin_id,
            "action": plugin_action,
            "params": params
        }
    
    def _evaluate_condition(self, condition: Dict[str, Any], 
                         context: Dict[str, Any]) -> bool:
        """评估条件表达式"""
        return Trigger._evaluate_condition(self, condition, context)
    
    def _get_value(self, path: str, context: Dict[str, Any]) -> Any:
        """获取值（支持嵌套路径）"""
        return Trigger._get_value(self, path, context)
    
    def add_next_step(self, step: 'Step'):
        """添加下一步骤"""
        self.next_steps.append(step)
    
    def add_prev_step(self, step: 'Step'):
        """添加上一步骤"""
        self.prev_steps.append(step)
    
    def set_parallel(self, parallel: bool = True):
        """设置是否并行执行"""
        self.parallel = parallel
    
    def set_continue_on_failure(self, should_continue: bool = True):
        """设置失败时是否继续"""
        self.continue_on_failure = should_continue
    
    def set_retry_times(self, times: int = 3):
        """设置重试次数"""
        self.retry_times = times
    
    def set_async(self, async_fn: Callable = None):
        """设置异步函数"""
        self.async_fn = async_fn
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "type": self.type.value,
            "name": self.name,
            "config": self.config,
            "parallel": self.parallel,
            "continue_on_failure": self.continue_on_failure,
            "retry_times": self.retry_times,
            "next_steps": [s.id for s in self.next_steps],
            "prev_steps": [s.id for s in self.prev_steps]
        }


class WorkflowEngine:
    """工作流引擎"""
    
    def __init__(self):
        """初始化工作流引擎"""
        self.workflows = {}
        self.triggers = []
        self.plugins = {}
        self.event_handlers = {}
    
    def create_workflow(self, workflow_id: str, name: str, 
                        description: str = "", version: str = "1.0"):
        """
        创建工作流
        
        Args:
            workflow_id: 工作流ID
            name: 工作流名称
            description: 描述
            version: 版本号
        """
        self.workflows[workflow_id] = {
            "id": workflow_id,
            "name": name,
            "description": description,
            "version": version,
            "steps": [],
            "created_at": datetime.now().isoformat()
        }
        
        print(f"创建工作流: {name} (ID: {workflow_id})")
        return workflow_id
    
    def add_trigger(self, workflow_id: str, trigger: Trigger):
        """
        添加触发器
        
        Args:
            workflow_id: 工作流ID
            trigger: 触发器对象
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"工作流不存在: {workflow_id}")
        
        self.workflows[workflow_id]["triggers"].append(trigger)
        print(f"为工作流 {workflow_id} 添加触发器: {trigger.id}")
    
    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        获取工作流
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            工作流字典
        """
        return self.workflows.get(workflow_id)
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        列出所有工作流
        
        Returns:
            工作流列表
        """
        return list(self.workflows.values())
    
    def execute_workflow(self, workflow_id: str, 
                         context: Dict[str, Any] = None,
                         async_mode: bool = False) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            workflow_id: 工流ID
            context: 上下文数据
            async_mode: 是否异步模式
            
        Returns:
            执行结果
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"工作流不存在: {workflow_id}")
        
        steps = workflow["steps"]
        if not steps:
            return {"success": True, "message": "工作流没有步骤"}
        
        current_context = context or {}
        
        for i, step in enumerate(steps):
            print(f"\n执行步骤 {i+1}/{len(steps)}: {step['name']}")
            
            step_obj = Step(
                step['id'],
                step['type'],
                step['name'],
                step.get('config')
            )
            
            try:
                result = step_obj.execute(current_context)
                current_context = {
                    **current_context,
                    f"step_{step['id']}_result": result
                }
                
                print(f"步骤 {step['id']} 执行结果: {result}")
                
            except Exception as e:
                print(f"步骤 {step['id']} 执行异常: {e}")
                
                if not step.continue_on_failure:
                    return {
                        "success": False,
                        "error": f"步骤 {step['id']} 失败: {str(e)}",
                        "failed_step": step['id']
                    }
                
                # 重试机制
                if step.retry_times > 0:
                    print(f"重试步骤 {step['id']}，剩余 {step.retry_times} 次")
                    try:
                        result = step_obj.execute(current_context)
                        current_context = {
                            **current_context,
                            f"step_{step['id']}_result": result
                        }
                    except Exception as e:
                        step.retry_times -= 1
                
                # 跳过失败的步骤
                continue
        
        print(f"\n工作流 {workflow_id} 执行完成")
        return {
            "success": True,
            "workflow_id": workflow_id,
            "context": current_context
        }
    
    def add_event_handler(self, event_type: str, handler: callable):
        """
        添加事件处理器
        
        Args:
            event_type: 事件类型
            handler: 处理函数
        """
        self.event_handlers[event_type] = handler
        print(f"添加事件处理器: {event_type}")
    
    def handle_event(self, event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理事件
        
        Args:
            event_type: 事件类型
            event_data: 事件数据
            
        Returns:
            处理结果
        """
        handler = self.event_handlers.get(event_type)
        if not handler:
            return {
                "success": False,
                "error": f"没有找到处理器: {event_type}"
            }
        
        try:
            result = handler(event_data)
            return {
                "success": True,
                "event_type": event_type,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "event_type": event_type,
                "error": str(e)
            }
    
    def add_plugin(self, plugin_id: str, plugin_config: Dict[str, Any]):
        """
        添加插件
        
        Args:
            plugin_id: 插件ID
            plugin_config: 插件配置
        """
        self.plugins[plugin_id] = plugin_config
        print(f"添加插件: {plugin_id}")
    
    def remove_plugin(self, plugin_id: str):
        """
        移除插件
        
        Args:
            plugin_id: 插件ID
        """
        if plugin_id in self.plugins:
            del self.plugins[plugin_id]
            print(f"移除插件: {plugin_id}")
    
    def export_workflow(self, workflow_id: str) -> str:
        """
        导出工作流为JSON
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            JSON字符串
        """
        workflow = self.get_workflow(workflow_id)
        return json.dumps(workflow, ensure_ascii=False, indent=2)
    
    def import_workflow(self, workflow_json: str) -> str:
        """
        导入工作流
        
        Args:
            workflow_json: JSON字符串
            
        Returns:
            工作流ID
        """
        workflow = json.loads(workflow_json)
        workflow_id = workflow.get('id')
        
        if not workflow_id:
            raise ValueError("工作流ID不能为空")
        
        self.workflows[workflow_id] = workflow
        print(f"导入工作流: {workflow_id}")
        
        return workflow_id
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            统计信息
        """
        return {
            "total_workflows": len(self.workflows),
            "total_triggers": sum(len(w.get('triggers', []) for w in self.workflows.values())),
            "total_plugins": len(self.plugins),
            "event_handlers": list(self.event_handlers.keys()),
            "created_workflows": [w['created_at'] for w in self.workflows.values()],
            "active_workflows": [w['id'] for w in self.workflows.values() if w.get('triggers')],
        }
