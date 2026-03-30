"""
微信插件
基于itchat-uos实现，支持个人微信消息发送、文件发送等功能
"""
import itchat
from itchat.content import TEXT, PICTURE, ATTACHMENT, VIDEO
from typing import Dict, Any, Optional
import os
from pathlib import Path

from rpa.core.plugin import BasePlugin, register_plugin


@register_plugin
class WechatMessagePlugin(BasePlugin):
    """微信消息插件"""
    plugin_name = "wechat/message"
    plugin_version = "1.0.0"
    plugin_description = "微信消息发送插件，支持给好友/群发送文本、图片、文件等"
    plugin_author = "三金的小虾米"
    
    # 全局登录状态
    _is_logged_in = False
    
    @classmethod
    def login(cls, hot_reload: bool = True):
        """登录微信"""
        if cls._is_logged_in:
            return True, "已经登录"
        
        try:
            itchat.auto_login(
                hotReload=hot_reload,
                statusStorageDir='wechat_session.pkl',
                enableCmdQR=2  # 命令行显示二维码
            )
            cls._is_logged_in = True
            return True, "登录成功"
        except Exception as e:
            return False, f"登录失败：{str(e)}"
    
    @classmethod
    def logout(cls):
        """退出登录"""
        if cls._is_logged_in:
            itchat.logout()
            cls._is_logged_in = False
            # 删除会话文件
            Path('wechat_session.pkl').unlink(missing_ok=True)
            return True, "已退出登录"
        return True, "未登录"
    
    @classmethod
    def search_contact(cls, name: str) -> Optional[Dict]:
        """搜索联系人/群聊"""
        if not cls._is_logged_in:
            success, msg = cls.login()
            if not success:
                return None
        
        # 搜索好友
        friends = itchat.search_friends(name=name)
        if friends:
            return friends[0]
        
        # 搜索群聊
        groups = itchat.search_chatrooms(name=name)
        if groups:
            return groups[0]
        
        # 搜索备注名/微信号
        friends = itchat.search_friends(remarkName=name)
        if friends:
            return friends[0]
        
        return None
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行插件动作
        
        Args:
            params:
                receiver: 接收人，好友昵称/备注/群名
                msg_type: 消息类型，text/picture/file/video
                content: 文本内容（text类型）
                file_path: 文件路径（picture/file/video类型）
                at_all: 是否@所有人（群聊时生效，默认False）
                hot_reload: 是否启用热重载，保持登录状态（默认True）
        
        Returns:
            执行结果
        """
        # 参数解析
        receiver = params.get('receiver')
        msg_type = params.get('msg_type', 'text').lower()
        content = params.get('content', '')
        file_path = params.get('file_path', '')
        at_all = params.get('at_all', False)
        hot_reload = params.get('hot_reload', True)
        
        if not receiver:
            return {
                'success': False,
                'error': '缺少必填参数：receiver'
            }
        
        # 登录
        if not self._is_logged_in:
            success, msg = self.login(hot_reload)
            if not success:
                return {
                    'success': False,
                    'error': msg
                }
        
        # 搜索接收人
        contact = self.search_contact(receiver)
        if not contact:
            return {
                'success': False,
                'error': f'未找到联系人/群：{receiver}'
            }
        
        user_name = contact['UserName']
        is_group = '@@' in user_name
        
        try:
            # 发送消息
            if msg_type == 'text':
                if not content:
                    return {'success': False, 'error': 'text类型需要content参数'}
                
                # 群聊@所有人
                if is_group and at_all:
                    content = f"@所有人 {content}"
                
                itchat.send(content, toUserName=user_name)
                return {
                    'success': True,
                    'result': '文本消息发送成功',
                    'receiver': receiver,
                    'content': content
                }
            
            elif msg_type in ['picture', 'image', 'img']:
                if not file_path or not os.path.exists(file_path):
                    return {'success': False, 'error': 'picture类型需要存在的file_path参数'}
                
                itchat.send_image(file_path, toUserName=user_name)
                return {
                    'success': True,
                    'result': '图片发送成功',
                    'receiver': receiver,
                    'file_path': file_path
                }
            
            elif msg_type in ['file', 'attachment']:
                if not file_path or not os.path.exists(file_path):
                    return {'success': False, 'error': 'file类型需要存在的file_path参数'}
                
                itchat.send_file(file_path, toUserName=user_name)
                return {
                    'success': True,
                    'result': '文件发送成功',
                    'receiver': receiver,
                    'file_path': file_path
                }
            
            elif msg_type == 'video':
                if not file_path or not os.path.exists(file_path):
                    return {'success': False, 'error': 'video类型需要存在的file_path参数'}
                
                itchat.send_video(file_path, toUserName=user_name)
                return {
                    'success': True,
                    'result': '视频发送成功',
                    'receiver': receiver,
                    'file_path': file_path
                }
            
            else:
                return {
                    'success': False,
                    'error': f'不支持的消息类型：{msg_type}'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'发送失败：{str(e)}'
            }


@register_plugin
class WechatContactPlugin(BasePlugin):
    """微信联系人插件"""
    plugin_name = "wechat/contact"
    plugin_version = "1.0.0"
    plugin_description = "微信联系人管理插件，支持获取好友列表、群列表"
    plugin_author = "三金的小虾米"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行动作
        
        Args:
            params:
                action: list_friends/list_groups/search
                keyword: 搜索关键词（search时必填）
        
        Returns:
            联系人列表
        """
        action = params.get('action', 'list_friends')
        keyword = params.get('keyword', '')
        
        # 登录
        if not WechatMessagePlugin._is_logged_in:
            success, msg = WechatMessagePlugin.login()
            if not success:
                return {'success': False, 'error': msg}
        
        try:
            if action == 'list_friends':
                friends = itchat.get_friends(update=True)
                friend_list = []
                for f in friends[1:]:  # 跳过自己
                    friend_list.append({
                        'nickname': f['NickName'],
                        'remark': f['RemarkName'],
                        'signature': f['Signature'],
                        'sex': f['Sex'],
                        'province': f['Province'],
                        'city': f['City']
                    })
                return {
                    'success': True,
                    'result': friend_list,
                    'count': len(friend_list)
                }
            
            elif action == 'list_groups':
                groups = itchat.get_chatrooms(update=True)
                group_list = []
                for g in groups:
                    group_list.append({
                        'name': g['NickName'],
                        'member_count': g['MemberCount']
                    })
                return {
                    'success': True,
                    'result': group_list,
                    'count': len(group_list)
                }
            
            elif action == 'search':
                if not keyword:
                    return {'success': False, 'error': 'search需要keyword参数'}
                
                contact = WechatMessagePlugin.search_contact(keyword)
                if contact:
                    return {
                        'success': True,
                        'result': {
                            'nickname': contact['NickName'],
                            'username': contact['UserName'],
                            'is_group': '@@' in contact['UserName']
                        }
                    }
                else:
                    return {'success': False, 'error': f'未找到联系人：{keyword}'}
            
            else:
                return {'success': False, 'error': f'不支持的action：{action}'}
        
        except Exception as e:
            return {'success': False, 'error': f'操作失败：{str(e)}'}
