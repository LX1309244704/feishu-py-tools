"""
基础插件库
"""
import os
import csv
import json
import shutil
from typing import Dict, Any, List
import pandas as pd
import requests
from rpa.core.plugin import BasePlugin, register_plugin


@register_plugin
class DataPlugin(BasePlugin):
    """数据处理插件"""
    
    plugin_name = "data/process"
    plugin_version = "1.0.0"
    plugin_description = "数据处理：过滤、统计、转换、聚合等"
    plugin_author = "三金的小虾米"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理数据
        
        Args:
            params:
                operation: 操作类型：filter/sort/aggregate/transform/join
                data: 输入数据
                ...其他参数根据操作类型而定
        """
        operation = params.get('operation')
        data = params.get('data', [])
        
        try:
            if operation == 'filter':
                condition = params.get('condition')
                filtered = [item for item in data if eval(condition, {}, {'item': item})]
                return {'success': True, 'data': filtered, 'count': len(filtered)}
            
            elif operation == 'sort':
                field = params.get('field')
                reverse = params.get('reverse', False)
                sorted_data = sorted(data, key=lambda x: x.get(field, ''), reverse=reverse)
                return {'success': True, 'data': sorted_data}
            
            elif operation == 'aggregate':
                field = params.get('field')
                func = params.get('function', 'sum')  # sum/avg/count/max/min
                values = [item.get(field, 0) for item in data if item.get(field) is not None]
                
                if func == 'sum':
                    result = sum(values)
                elif func == 'avg':
                    result = sum(values) / len(values) if values else 0
                elif func == 'count':
                    result = len(values)
                elif func == 'max':
                    result = max(values) if values else None
                elif func == 'min':
                    result = min(values) if values else None
                elif func == 'count_unique':
                    result = len(set(values))
                else:
                    return {'success': False, 'error': f'不支持的聚合函数: {func}'}
                
                return {'success': True, 'result': result}
            
            elif operation == 'transform':
                mapping = params.get('mapping', {})
                transformed = []
                for item in data:
                    new_item = {}
                    for new_key, expr in mapping.items():
                        new_item[new_key] = eval(expr, {}, {'item': item})
                    transformed.append(new_item)
                return {'success': True, 'data': transformed}
            
            elif operation == 'deduplicate':
                field = params.get('field')
                seen = set()
                unique = []
                for item in data:
                    value = item.get(field)
                    if value not in seen:
                        seen.add(value)
                        unique.append(item)
                return {'success': True, 'data': unique, 'removed': len(data) - len(unique)}
            
            else:
                return {'success': False, 'error': f'不支持的operation: {operation}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


@register_plugin
class FilePlugin(BasePlugin):
    """文件操作插件"""
    
    plugin_name = "file/operation"
    plugin_version = "1.0.0"
    plugin_description = "文件操作：读写、复制、移动、删除、压缩等"
    plugin_author = "三金的小虾米"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        action = params.get('action')
        path = params.get('path')
        
        if not action or not path:
            return {'success': False, 'error': '缺少action或path参数'}
        
        try:
            if action == 'read':
                encoding = params.get('encoding', 'utf-8')
                with open(path, 'r', encoding=encoding) as f:
                    content = f.read()
                return {'success': True, 'content': content}
            
            elif action == 'write':
                content = params.get('content', '')
                encoding = params.get('encoding', 'utf-8')
                append = params.get('append', False)
                mode = 'a' if append else 'w'
                with open(path, mode, encoding=encoding) as f:
                    f.write(content)
                return {'success': True, 'size': len(content)}
            
            elif action == 'read_csv':
                df = pd.read_csv(path)
                data = df.to_dict('records')
                return {'success': True, 'data': data, 'rows': len(data)}
            
            elif action == 'write_csv':
                data = params.get('data', [])
                df = pd.DataFrame(data)
                df.to_csv(path, index=False)
                return {'success': True, 'rows': len(data)}
            
            elif action == 'read_excel':
                sheet_name = params.get('sheet_name', 0)
                df = pd.read_excel(path, sheet_name=sheet_name)
                data = df.to_dict('records')
                return {'success': True, 'data': data, 'rows': len(data)}
            
            elif action == 'write_excel':
                data = params.get('data', [])
                sheet_name = params.get('sheet_name', 'Sheet1')
                df = pd.DataFrame(data)
                df.to_excel(path, sheet_name=sheet_name, index=False)
                return {'success': True, 'rows': len(data)}
            
            elif action == 'exists':
                exists = os.path.exists(path)
                is_file = os.path.isfile(path)
                is_dir = os.path.isdir(path)
                return {'success': True, 'exists': exists, 'is_file': is_file, 'is_dir': is_dir}
            
            elif action == 'delete':
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                return {'success': True}
            
            elif action == 'copy':
                target = params['target']
                shutil.copy2(path, target)
                return {'success': True}
            
            elif action == 'move':
                target = params['target']
                shutil.move(path, target)
                return {'success': True}
            
            elif action == 'list_dir':
                files = os.listdir(path)
                return {'success': True, 'files': files, 'count': len(files)}
            
            elif action == 'mkdir':
                exist_ok = params.get('exist_ok', True)
                os.makedirs(path, exist_ok=exist_ok)
                return {'success': True}
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


@register_plugin
class HttpPlugin(BasePlugin):
    """HTTP请求插件"""
    
    plugin_name = "http/request"
    plugin_version = "1.0.0"
    plugin_description = "HTTP请求：GET/POST/PUT/DELETE等"
    plugin_author = "三金的小虾米"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        url = params.get('url')
        method = params.get('method', 'GET').upper()
        
        if not url:
            return {'success': False, 'error': '缺少url参数'}
        
        try:
            kwargs = {
                'timeout': params.get('timeout', 30),
                'headers': params.get('headers', {}),
                'verify': params.get('verify', True)
            }
            
            if params.get('params'):
                kwargs['params'] = params['params']
            
            if params.get('json'):
                kwargs['json'] = params['json']
            
            if params.get('data'):
                kwargs['data'] = params['data']
            
            if params.get('auth'):
                kwargs['auth'] = tuple(params['auth'])
            
            response = requests.request(method, url, **kwargs)
            
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            return {
                'success': True,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'data': response_data,
                'text': response.text
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
