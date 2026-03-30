"""
AI增强插件
支持大模型调用，文本生成、摘要、分类、翻译等AI能力
"""
import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI
import anthropic
import dashscope
from http import HTTPStatus

from rpa.core.plugin import BasePlugin, register_plugin


@register_plugin
class AIPlugin(BasePlugin):
    """AI增强插件"""
    plugin_name = "ai/llm"
    plugin_version = "1.0.0"
    plugin_description = "AI大模型插件，支持GPT、Claude、通义千问等大模型调用"
    plugin_author = "三金的小虾米"
    
    def _get_openai_client(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """获取OpenAI客户端"""
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        base_url = base_url or os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        if not api_key:
            raise ValueError("OPENAI_API_KEY未配置")
        return OpenAI(api_key=api_key, base_url=base_url)
    
    def _get_anthropic_client(self, api_key: Optional[str] = None):
        """获取Anthropic客户端"""
        api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY未配置")
        return anthropic.Anthropic(api_key=api_key)
    
    def _call_openai(self, messages: List[Dict], model: str = 'gpt-3.5-turbo', 
                   temperature: float = 0.7, max_tokens: Optional[int] = None,
                   api_key: Optional[str] = None, base_url: Optional[str] = None) -> Dict:
        """调用OpenAI API"""
        client = self._get_openai_client(api_key, base_url)
        params = {
            'model': model,
            'messages': messages,
            'temperature': temperature
        }
        if max_tokens:
            params['max_tokens'] = max_tokens
        
        response = client.chat.completions.create(**params)
        return {
            'content': response.choices[0].message.content,
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            },
            'model': response.model
        }
    
    def _call_anthropic(self, messages: List[Dict], model: str = 'claude-3-sonnet-20240229',
                       temperature: float = 0.7, max_tokens: int = 1024,
                       api_key: Optional[str] = None) -> Dict:
        """调用Anthropic Claude API"""
        client = self._get_anthropic_client(api_key)
        
        # 转换消息格式
        system_prompt = None
        claude_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                system_prompt = msg['content']
            else:
                claude_messages.append(msg)
        
        params = {
            'model': model,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'messages': claude_messages
        }
        if system_prompt:
            params['system'] = system_prompt
        
        response = client.messages.create(**params)
        return {
            'content': response.content[0].text,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens
            },
            'model': response.model
        }
    
    def _call_qwen(self, messages: List[Dict], model: str = 'qwen-plus',
                  temperature: float = 0.7, max_tokens: Optional[int] = None,
                  api_key: Optional[str] = None) -> Dict:
        """调用通义千问API"""
        api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY未配置")
        dashscope.api_key = api_key
        
        params = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'result_format': 'message'
        }
        if max_tokens:
            params['max_tokens'] = max_tokens
        
        response = dashscope.Generation.call(**params)
        if response.status_code != HTTPStatus.OK:
            raise Exception(f"通义千问调用失败: {response.message}")
        
        return {
            'content': response.output.choices[0].message.content,
            'usage': response.usage,
            'model': model
        }
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行AI操作
        
        Args:
            params:
                action: 操作类型
                    - chat: 聊天对话
                    - generate: 文本生成
                    - summarize: 文本摘要
                    - translate: 翻译
                    - classify: 文本分类
                    - extract: 信息抽取
                provider: 服务商：openai/anthropic/qwen
                model: 模型名称
                messages: 对话消息列表（chat时必填）
                prompt: 提示词（generate/summarize/translate等时必填）
                input: 输入文本（summarize/translate/classify/extract时必填）
                temperature: 温度，默认0.7
                max_tokens: 最大生成token数
                api_key: 可选，API密钥，默认从环境变量读取
                base_url: 可选，API地址（仅openai支持）
                system_prompt: 可选，系统提示词
        """
        action = params.get('action', 'chat')
        provider = params.get('provider', 'openai')
        model = params.get('model')
        temperature = params.get('temperature', 0.7)
        max_tokens = params.get('max_tokens')
        api_key = params.get('api_key')
        base_url = params.get('base_url')
        system_prompt = params.get('system_prompt')
        
        try:
            # 构建消息
            messages = []
            if system_prompt:
                messages.append({'role': 'system', 'content': system_prompt})
            
            if action == 'chat':
                input_messages = params.get('messages', [])
                if not input_messages:
                    return {'success': False, 'error': '缺少messages参数'}
                messages.extend(input_messages)
            
            elif action == 'generate':
                prompt = params.get('prompt')
                if not prompt:
                    return {'success': False, 'error': '缺少prompt参数'}
                messages.append({'role': 'user', 'content': prompt})
            
            elif action == 'summarize':
                input_text = params.get('input')
                if not input_text:
                    return {'success': False, 'error': '缺少input参数'}
                prompt = f"请总结以下文本的核心内容，要求简洁明了：\n{input_text}"
                messages.append({'role': 'user', 'content': prompt})
            
            elif action == 'translate':
                input_text = params.get('input')
                target_lang = params.get('target_lang', '中文')
                if not input_text:
                    return {'success': False, 'error': '缺少input参数'}
                prompt = f"请将以下文本翻译成{target_lang}：\n{input_text}"
                messages.append({'role': 'user', 'content': prompt})
            
            elif action == 'classify':
                input_text = params.get('input')
                categories = params.get('categories', [])
                if not input_text or not categories:
                    return {'success': False, 'error': '缺少input或categories参数'}
                categories_str = '、'.join(categories)
                prompt = f"请将以下文本分类，可选类别：{categories_str}，只返回类别名称：\n{input_text}"
                messages.append({'role': 'user', 'content': prompt})
            
            elif action == 'extract':
                input_text = params.get('input')
                fields = params.get('fields', [])
                if not input_text or not fields:
                    return {'success': False, 'error': '缺少input或fields参数'}
                fields_str = '、'.join(fields)
                prompt = f"请从以下文本中提取这些信息：{fields_str}，返回JSON格式：\n{input_text}"
                messages.append({'role': 'user', 'content': prompt})
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
            
            # 调用对应服务商API
            if provider == 'openai':
                if not model:
                    model = 'gpt-3.5-turbo'
                result = self._call_openai(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    api_key=api_key,
                    base_url=base_url
                )
            
            elif provider == 'anthropic':
                if not model:
                    model = 'claude-3-sonnet-20240229'
                result = self._call_anthropic(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens or 1024,
                    api_key=api_key
                )
            
            elif provider == 'qwen':
                if not model:
                    model = 'qwen-plus'
                result = self._call_qwen(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    api_key=api_key
                )
            
            else:
                return {'success': False, 'error': f'不支持的服务商: {provider}'}
            
            return {
                'success': True,
                'content': result['content'],
                'usage': result['usage'],
                'model': result['model'],
                'provider': provider
            }
        
        except Exception as e:
            return {'success': False, 'error': f'AI调用失败: {str(e)}'}
