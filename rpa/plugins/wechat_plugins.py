"""
微信插件
"""
import os
from typing import Dict, Any, Optional
from rpa.core.plugin import BasePlugin, register_plugin

# 这些是占位符，实际使用时需要安装对应的库
# import wechatpy  # 需要安装: pip install wechatpy
# from wechatpy.client import WeChatClient
# from wechatpy.client.api import WeChatMessage, WeChatUser
# from wechatpy.work import WeChatWork, WeChatWorkChat, WeChatWorkDepartment, WeChatWorkUser
# from wechatpy.storage.memory import MemoryStorage


@register_plugin
class WechatWorkPlugin(BasePlugin):
    """企业微信插件"""
    plugin_name = "wechat/work"
    plugin_version = "1.0.0"
    plugin_description = "企业微信插件，支持消息发送、通讯录管理、客户联系等"
    plugin_author = "三金的小虾米"
    
    def _get_client(self, corp_id: str, corp_secret: str, agent_id: Optional[int] = None):
        """获取企业微信客户端（需要安装wechatpy）"""
        try:
            from wechatpy.work import WeChatWork
            return WeChatWork(corp_id, corp_secret, agent_id)
        except ImportError:
            raise ImportError("需要安装wechatpy: pip install wechatpy")
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行企业微信操作
        
        Args:
            params:
                action: 操作类型
                    - send_text: 发送文本消息
                    - send_markdown: 发送Markdown消息
                    - get_user_list: 获取部门用户列表
                    - get_department_list: 获取部门列表
                corp_id: 企业ID（必填）
                corp_secret: 应用Secret（必填）
                agent_id: 应用ID（发送消息时必填）
                receiver: 接收人，userid列表，@all表示全员
                content: 消息内容
        """
        action = params.get('action')
        corp_id = params.get('corp_id') or os.getenv('WECHAT_WORK_CORP_ID')
        corp_secret = params.get('corp_secret') or os.getenv('WECHAT_WORK_CORP_SECRET')
        agent_id = params.get('agent_id') or os.getenv('WECHAT_WORK_AGENT_ID')
        
        if not corp_id or not corp_secret:
            return {'success': False, 'error': '缺少corp_id或corp_secret参数'}
        
        try:
            client = self._get_client(corp_id, corp_secret, agent_id)
            
            if action in ['send_text', 'send_markdown']:
                if not agent_id:
                    return {'success': False, 'error': '发送消息需要agent_id参数'}
                
                receiver = params.get('receiver', '@all')
                to_user = receiver if receiver != '@all' else None
                to_all = receiver == '@all'
                content = params.get('content')
                
                if not content:
                    return {'success': False, 'error': '缺少content参数'}
                
                if action == 'send_text':
                    result = client.message.send_text(
                        agent_id=agent_id,
                        content=content,
                        to_user=to_user,
                        to_all=to_all
                    )
                else:
                    result = client.message.send_markdown(
                        agent_id=agent_id,
                        content=content,
                        to_user=to_user,
                        to_all=to_all
                    )
                
                return {'success': True, 'result': f'{action}消息发送成功', 'response': result}
            
            elif action == 'get_user_list':
                department_id = params.get('department_id', 1)
                result = client.user.list(department_id)
                return {
                    'success': True,
                    'user_list': result['userlist'],
                    'count': len(result.get('userlist', []))
                }
            
            elif action == 'get_department_list':
                result = client.department.list()
                return {
                    'success': True,
                    'department_list': result.get('department', []),
                    'count': len(result.get('department', []))
                }
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
        
        except ImportError as e:
            return {'success': False, 'error': f'请先安装wechatpy: pip install wechatpy'}
        except Exception as e:
            return {'success': False, 'error': f'企业微信操作失败: {str(e)}'}


@register_plugin
class WechatMpPlugin(BasePlugin):
    """微信公众号插件"""
    plugin_name = "wechat/mp"
    plugin_version = "1.0.0"
    plugin_description = "微信公众号插件，支持模板消息、客服消息等"
    plugin_author = "三金的小虾米"
    
    def _get_client(self, app_id: str, app_secret: str):
        """获取公众号客户端（需要安装wechatpy）"""
        try:
            from wechatpy.client import WeChatClient
            from wechatpy.storage.memory import MemoryStorage
            return WeChatClient(app_id, app_secret, session=MemoryStorage())
        except ImportError:
            raise ImportError("需要安装wechatpy: pip install wechatpy")
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行公众号操作
        
        Args:
            params:
                action: 操作类型
                    - send_template: 发送模板消息
                    - get_user_info: 获取用户信息
                    - create_menu: 创建自定义菜单
                app_id: 公众号AppID（必填）
                app_secret: 公众号AppSecret（必填）
                openid: 用户openid
                template_id: 模板ID
                data: 模板数据
                menus: 菜单配置
        """
        action = params.get('action')
        app_id = params.get('app_id') or os.getenv('WECHAT_MP_APP_ID')
        app_secret = params.get('app_secret') or os.getenv('WECHAT_MP_APP_SECRET')
        
        if not app_id or not app_secret:
            return {'success': False, 'error': '缺少app_id或app_secret参数'}
        
        try:
            client = self._get_client(app_id, app_secret)
            
            if action == 'send_template':
                openid = params.get('openid')
                template_id = params.get('template_id')
                data = params.get('data', {})
                
                if not openid or not template_id:
                    return {'success': False, 'error': '缺少openid或template_id参数'}
                
                result = client.message.send_template(
                    openid,
                    template_id,
                    data=data,
                    url=params.get('url')
                )
                return {'success': True, 'result': '模板消息发送成功', 'msg_id': result.get('msgid')}
            
            elif action == 'get_user_info':
                openid = params.get('openid')
                if not openid:
                    return {'success': False, 'error': '缺少openid参数'}
                user_info = client.user.get(openid)
                return {'success': True, 'user_info': user_info}
            
            elif action == 'create_menu':
                menus = params.get('menus')
                if not menus:
                    return {'success': False, 'error': '缺少menus参数'}
                result = client.menu.create(menus)
                return {'success': True, 'result': '菜单创建成功'}
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
        
        except ImportError:
            return {'success': False, 'error': '请先安装wechatpy: pip install wechatpy'}
        except Exception as e:
            return {'success': False, 'error': f'公众号操作失败: {str(e)}'}
