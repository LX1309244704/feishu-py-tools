"""
RPA执行引擎
"""
import time
import traceback
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from .flow import Flow
from .variable_engine import variable_engine
from .plugin import get_plugin


class ExecutionEngine:
    """流程执行引擎"""
    
    def __init__(self, max_workers: int = 5):
        """
        初始化执行引擎
        
        Args:
            max_workers: 最大并行执行线程数
        """
        self.max_workers = max_workers
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("rpa.engine")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def execute_flow(self, flow: Flow, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行完整流程
        
        Args:
            flow: 流程对象
            context: 初始上下文数据
            
        Returns:
            执行结果
        """
        start_time = datetime.now()
        flow_id = f"{flow.name}_{int(start_time.timestamp())}"
        self.logger.info(f"开始执行流程: {flow.name} (ID: {flow_id})")
        
        # 初始化上下文
        context = context or {}
        context['flow'] = flow.to_dict()
        context['env'] = {}  # 环境变量
        context['steps'] = {}  # 步骤输出结果
        context['globals'] = flow.variables  # 全局变量
        
        execution_result = {
            'flow_id': flow_id,
            'flow_name': flow.name,
            'start_time': start_time.isoformat(),
            'status': 'running',
            'steps': [],
            'error': None
        }
        
        try:
            # 执行主步骤
            success = self._execute_steps(flow.steps, context, execution_result['steps'])
            
            if success:
                # 执行成功回调
                if flow.on_success:
                    self.logger.info("执行成功回调步骤")
                    self._execute_steps(flow.on_success, context, execution_result['steps'])
                
                execution_result['status'] = 'success'
                self.logger.info(f"流程执行成功: {flow.name}")
            else:
                # 执行失败回调
                if flow.on_failure:
                    self.logger.info("执行失败回调步骤")
                    self._execute_steps(flow.on_failure, context, execution_result['steps'])
                
                execution_result['status'] = 'failed'
                self.logger.error(f"流程执行失败: {flow.name}")
        
        except Exception as e:
            execution_result['status'] = 'failed'
            execution_result['error'] = str(e)
            execution_result['traceback'] = traceback.format_exc()
            self.logger.error(f"流程执行异常: {str(e)}")
            self.logger.debug(traceback.format_exc())
        
        finally:
            end_time = datetime.now()
            execution_result['end_time'] = end_time.isoformat()
            execution_result['duration'] = (end_time - start_time).total_seconds()
            execution_result['context'] = context
        
        return execution_result
    
    def _execute_steps(self, steps: List[Dict[str, Any]], context: Dict[str, Any], 
                     steps_result: List[Dict[str, Any]]) -> bool:
        """
        执行步骤列表
        
        Args:
            steps: 步骤列表
            context: 上下文
            steps_result: 步骤执行结果列表
            
        Returns:
            是否全部执行成功
        """
        # 分离并行和串行步骤
        parallel_steps = [s for s in steps if s.get('parallel', False)]
        serial_steps = [s for s in steps if not s.get('parallel', False)]
        
        # 先执行并行步骤
        if parallel_steps:
            self.logger.info(f"开始执行并行步骤: {len(parallel_steps)}个")
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self._execute_single_step, step, context.copy()): step 
                    for step in parallel_steps
                }
                
                for future in as_completed(futures):
                    step = futures[future]
                    try:
                        result = future.result()
                        steps_result.append(result)
                        # 合并步骤结果到上下文
                        context['steps'][step['name']] = result
                        
                        if not result['success'] and not step.get('continue_on_failure', False):
                            self.logger.error(f"并行步骤失败: {step['name']}")
                            return False
                            
                    except Exception as e:
                        self.logger.error(f"并行步骤异常: {step['name']}: {str(e)}")
                        return False
        
        # 再执行串行步骤
        for step in serial_steps:
            result = self._execute_single_step(step, context)
            steps_result.append(result)
            
            # 合并步骤结果到上下文
            context['steps'][step['name']] = result
            
            if not result['success']:
                if not step.get('continue_on_failure', False):
                    self.logger.error(f"步骤执行失败: {step['name']}")
                    return False
                else:
                    self.logger.warning(f"步骤执行失败但继续: {step['name']}")
        
        return True
    
    def _execute_single_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个步骤
        
        Args:
            step: 步骤配置
            context: 上下文
            
        Returns:
            步骤执行结果
        """
        step_name = step['name']
        start_time = datetime.now()
        self.logger.info(f"开始执行步骤: {step_name}")
        
        result = {
            'name': step_name,
            'start_time': start_time.isoformat(),
            'status': 'running',
            'output': None,
            'error': None
        }
        
        try:
            # 检查步骤执行条件
            if 'if' in step:
                condition = step['if']
                if not variable_engine.evaluate_expression(condition, context):
                    result['status'] = 'skipped'
                    result['message'] = f"条件不满足: {condition}"
                    self.logger.info(f"跳过步骤: {step_name}，条件不满足")
                    return result
            
            # 渲染步骤参数
            params = variable_engine.render(step.get('with', {}), context)
            self.logger.debug(f"步骤参数: {params}")
            
            # 获取插件
            plugin_ref = step['uses']
            plugin_class = get_plugin(plugin_ref)
            if not plugin_class:
                raise ValueError(f"插件不存在: {plugin_ref}")
            
            plugin = plugin_class()
            plugin.logger = self.logger
            
            # 参数校验
            plugin.validate_params(params)
            
            # 重试逻辑
            retry_times = step.get('retry', 0)
            timeout = step.get('timeout', 300)
            attempt = 0
            success = False
            output = None
            
            while attempt <= retry_times and not success:
                if attempt > 0:
                    self.logger.info(f"步骤重试: {step_name}，第{attempt}次")
                    time.sleep(min(attempt * 2, 10))  # 指数退避
                
                try:
                    output = plugin.execute(params, context)
                    success = output.get('success', True)
                    if not success:
                        error_msg = output.get('error', '未知错误')
                        self.logger.warning(f"步骤执行失败: {error_msg}")
                except Exception as e:
                    error_msg = str(e)
                    self.logger.warning(f"步骤执行异常: {error_msg}")
                    output = {'success': False, 'error': error_msg}
                
                attempt += 1
            
            if not success:
                result['status'] = 'failed'
                result['error'] = output.get('error', '未知错误')
                self.logger.error(f"步骤执行失败: {step_name}，错误: {result['error']}")
            else:
                result['status'] = 'success'
                result['output'] = output
                self.logger.info(f"步骤执行成功: {step_name}")
        
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
            self.logger.error(f"步骤执行异常: {step_name}: {str(e)}")
            self.logger.debug(traceback.format_exc())
        
        finally:
            end_time = datetime.now()
            result['end_time'] = end_time.isoformat()
            result['duration'] = (end_time - start_time).total_seconds()
        
        return result
    
    def execute_step(self, step_config: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """单独执行单个步骤"""
        context = context or {}
        return self._execute_single_step(step_config, context)


# 全局执行引擎实例
execution_engine = ExecutionEngine()

__all__ = ['ExecutionEngine', 'execution_engine']
