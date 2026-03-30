"""
Lark CLI 官方工具插件
让微元可以调用飞书官方 CLI，享受 200+ 命令和自动 API 同步
"""
import subprocess
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

from rpa.core.plugin import BasePlugin, register_plugin


@register_plugin
class LarkCliPlugin(BasePlugin):
    """飞书官方 CLI 插件"""
    plugin_name = "lark/cli"
    plugin_version = "1.0.0"
    plugin_description = "调用飞书官方 CLI (lark-cli)，支持 200+ 命令和自动 API 同步"
    plugin_author = "三金的小虾米"
    
    def _run_lark_cli(self, args: List[str], capture_output: bool = True) -> Dict[str, Any]:
        """
        执行 lark-cli 命令
        
        Args:
            args: 命令参数列表
            capture_output: 是否捕获输出
        
        Returns:
            执行结果
        """
        try:
            # 检查 lark-cli 是否安装
            result = subprocess.run(
                ["lark-cli", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': 'lark-cli 未安装，请先运行：npm install -g @larksuite/cli'
                }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'lark-cli 未找到，请先安装：npm install -g @larksuite/cli'
            }
        
        # 执行命令
        try:
            cmd = ["lark-cli"] + args
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # 尝试解析 JSON 输出
                try:
                    output_json = json.loads(result.stdout)
                except json.JSONDecodeError:
                    output_json = None
                
                return {
                    'success': True,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'json': output_json
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr or result.stdout,
                    'returncode': result.returncode
                }
        
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '命令执行超时（60秒）'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'执行失败：{str(e)}'
            }
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行官方 CLI 命令
        
        Args:
            params:
                command: 命令类型
                    - shortcut: 快捷命令（如 calendar +agenda）
                    - api: API 命令（如 calendar calendars list）
                    - generic: 通用 API 调用（如 api GET /path）
                    - auth: 认证相关
                service: 服务名（calendar/im/doc/base等）
                shortcut: 快捷命令名（+agenda/+messages-send等）
                method: API 方法（get/list/create等）
                endpoint: 通用 API 端点路径
                params: 请求参数（JSON字符串或字典）
                body: 请求体（JSON字符串或字典）
                format: 输出格式（json/pretty/table/ndjson/csv）
                dry_run: 是否仅预览（不实际执行）
                args: 额外参数列表
        
        Returns:
            执行结果
        """
        command = params.get('command', 'shortcut')
        service = params.get('service', '')
        format_type = params.get('format', 'json')
        dry_run = params.get('dry_run', False)
        extra_args = params.get('args', [])
        
        try:
            if command == 'shortcut':
                # 快捷命令：lark-cli <service> +<shortcut>
                shortcut = params.get('shortcut', '')
                if not service or not shortcut:
                    return {'success': False, 'error': 'shortcut 命令需要 service 和 shortcut 参数'}
                
                args = [service, shortcut, '--format', format_type]
                
                # 添加其他参数
                cmd_params = params.get('params', {})
                for key, value in cmd_params.items():
                    args.extend([f'--{key}', str(value)])
                
                if dry_run:
                    args.append('--dry-run')
                
                args.extend(extra_args)
                return self._run_lark_cli(args)
            
            elif command == 'api':
                # API 命令：lark-cli <service> <method>
                method = params.get('method', '')
                if not service or not method:
                    return {'success': False, 'error': 'api 命令需要 service 和 method 参数'}
                
                args = [service, method, '--format', format_type]
                
                # 添加参数
                cmd_params = params.get('params', {})
                if isinstance(cmd_params, dict):
                    args.extend(['--params', json.dumps(cmd_params, ensure_ascii=False)])
                elif isinstance(cmd_params, str):
                    args.extend(['--params', cmd_params])
                
                if dry_run:
                    args.append('--dry-run')
                
                args.extend(extra_args)
                return self._run_lark_cli(args)
            
            elif command == 'generic':
                # 通用 API：lark-cli api <HTTP_METHOD> <ENDPOINT>
                http_method = params.get('http_method', 'GET')
                endpoint = params.get('endpoint', '')
                if not endpoint:
                    return {'success': False, 'error': 'generic 命令需要 endpoint 参数'}
                
                args = ['api', http_method, endpoint]
                
                # 添加 params 和 body
                cmd_params = params.get('params', {})
                if cmd_params:
                    if isinstance(cmd_params, dict):
                        args.extend(['--params', json.dumps(cmd_params, ensure_ascii=False)])
                    else:
                        args.extend(['--params', cmd_params])
                
                body = params.get('body', {})
                if body:
                    if isinstance(body, dict):
                        args.extend(['--body', json.dumps(body, ensure_ascii=False)])
                    else:
                        args.extend(['--body', body])
                
                if format_type != 'json':
                    args.extend(['--format', format_type])
                
                args.extend(extra_args)
                return self._run_lark_cli(args)
            
            elif command == 'auth':
                # 认证命令
                auth_action = params.get('auth_action', 'status')
                args = ['auth', auth_action]
                
                if auth_action == 'login':
                    domain = params.get('domain', '')
                    scope = params.get('scope', '')
                    if domain:
                        args.extend(['--domain', domain])
                    if scope:
                        args.extend(['--scope', scope])
                    if params.get('recommend', False):
                        args.append('--recommend')
                
                args.extend(extra_args)
                return self._run_lark_cli(args)
            
            elif command == 'raw':
                # 原始命令，直接传递参数
                raw_args = params.get('raw_args', [])
                return self._run_lark_cli(raw_args)
            
            else:
                return {'success': False, 'error': f'不支持的命令类型：{command}'}
        
        except Exception as e:
            return {'success': False, 'error': f'执行异常：{str(e)}'}


@register_plugin
class LarkCliSkillPlugin(BasePlugin):
    """飞书官方 CLI Skill 插件"""
    plugin_name = "lark/skill"
    plugin_version = "1.0.0"
    plugin_description = "调用飞书官方 CLI Skill，如 lark-calendar/lark-im 等"
    plugin_author = "三金的小虾米"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 Skill 命令
        
        Args:
            params:
                skill: Skill 名称（如 lark-calendar, lark-im）
                action: 动作名称
                args: 其他参数
        """
        skill = params.get('skill', '')
        action = params.get('action', '')
        args = params.get('args', [])
        
        if not skill:
            return {'success': False, 'error': '需要指定 skill 参数'}
        
        try:
            # 使用 npx skills 执行
            cmd = ['npx', 'skills', skill]
            if action:
                cmd.append(action)
            cmd.extend(args)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output': result.stdout,
                    'skill': skill,
                    'action': action
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr or result.stdout,
                    'skill': skill
                }
        
        except Exception as e:
            return {'success': False, 'error': f'Skill 执行失败：{str(e)}'}
