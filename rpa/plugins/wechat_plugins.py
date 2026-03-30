
@register_plugin
class WechatWorkPlugin(BasePlugin):
    """企业微信插件"""
    plugin_name = "wechat/work"
    plugin_version = "1.0.0"
    plugin_description = "企业微信插件，支持消息发送、通讯录管理、客户联系等"
    plugin_author = "三金的小虾米"
    
    def _get_client(self, corp_id: str, corp_secret: str, agent_id: Optional[int] = None):
        """获取企业微信客户端"""
        return WeChatWork(corp_id, corp_secret, agent_id)
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行企业微信操作
        
        Args:
            params:
                action: 操作类型
                    - send_text: 发送文本消息
                    - send_image: 发送图片
                    - send_file: 发送文件
                    - send_markdown: 发送Markdown消息
                    - get_user_list: 获取部门用户列表
                    - get_department_list: 获取部门列表
                    - send_to_group: 发送群消息
                corp_id: 企业ID（必填）
                corp_secret: 应用Secret（必填）
                agent_id: 应用ID（发送消息时必填）
                receiver: 接收人，userid列表，多个用|分隔，或者@all
                content: 消息内容
                media_path: 媒体文件路径（发送图片/文件时必填）
                department_id: 部门ID（获取用户列表时可选）
        """
        action = params.get('action')
        corp_id = params.get('corp_id') or os.getenv('WECHAT_WORK_CORP_ID')
        corp_secret = params.get('corp_secret') or os.getenv('WECHAT_WORK_CORP_SECRET')
        agent_id = params.get('agent_id') or os.getenv('WECHAT_WORK_AGENT_ID')
        
        if not corp_id or not corp_secret:
            return {'success': False, 'error': '缺少corp_id或corp_secret参数'}
        
        try:
            client = self._get_client(corp_id, corp_secret, agent_id)
            
            if action in ['send_text', 'send_image', 'send_file', 'send_markdown']:
                if not agent_id:
                    return {'success': False, 'error': '发送消息需要agent_id参数'}
                
                receiver = params.get('receiver', '@all')
                to_user = receiver if receiver != '@all' else None
                to_all = receiver == '@all'
                
                if action == 'send_text':
                    content = params.get('content')
                    if not content:
                        return {'success': False, 'error': '缺少content参数'}
                    result = client.message.send_text(
                        agent_id=agent_id,
                        content=content,
                        to_user=to_user,
                        to_all=to_all
                    )
                    return {'success': True, 'result': '文本消息发送成功', 'response': result}
                
                elif action == 'send_markdown':
                    content = params.get('content')
                    if not content:
                        return {'success': False, 'error': '缺少content参数'}
                    result = client.message.send_markdown(
                        agent_id=agent_id,
                        content=content,
                        to_user=to_user,
                        to_all=to_all
                    )
                    return {'success': True, 'result': 'Markdown消息发送成功', 'response': result}
                
                elif action in ['send_image', 'send_file']:
                    media_path = params.get('media_path')
                    if not media_path or not os.path.exists(media_path):
                        return {'success': False, 'error': 'media_path不存在'}
                    
                    # 上传媒体文件
                    media_type = 'image' if action == 'send_image' else 'file'
                    upload_result = client.media.upload(media_type, open(media_path, 'rb'))
                    media_id = upload_result['media_id']
                    
                    if action == 'send_image':
                        result = client.message.send_image(
                            agent_id=agent_id,
                            media_id=media_id,
                            to_user=to_user,
                            to_all=to_all
                        )
                    else:
                        result = client.message.send_file(
                            agent_id=agent_id,
                            media_id=media_id,
                            to_user=to_user,
                            to_all=to_all
                        )
                    
                    return {'success': True, 'result': f'{media_type}发送成功', 'media_id': media_id, 'response': result}
            
            elif action == 'get_user_list':
                department_id = params.get('department_id', 1)
                fetch_child = params.get('fetch_child', 1)
                result = client.user.list(department_id, fetch_child=fetch_child)
                return {
                    'success': True,
                    'user_list': result['userlist'],
                    'count': len(result['userlist'])
                }
            
            elif action == 'get_department_list':
                result = client.department.list()
                return {
                    'success': True,
                    'department_list': result['department'],
                    'count': len(result['department'])
                }
            
            elif action == 'send_to_group':
                chat_id = params.get('chat_id')
                msg_type = params.get('msg_type', 'text')
                content = params.get('content')
                if not chat_id or not content:
                    return {'success': False, 'error': '缺少chat_id或content参数'}
                
                if msg_type == 'text':
                    result = client.message.send_text(agent_id=agent_id, content=content, chat_id=chat_id)
                elif msg_type == 'markdown':
                    result = client.message.send_markdown(agent_id=agent_id, content=content, chat_id=chat_id)
                else:
                    return {'success': False, 'error': f'不支持的消息类型: {msg_type}'}
                
                return {'success': True, 'result': '群消息发送成功', 'response': result}
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
        
        except Exception as e:
            return {'success': False, 'error': f'企业微信操作失败: {str(e)}'}


@register_plugin
class WechatMpPlugin(BasePlugin):
    """微信公众号插件"""
    plugin_name = "wechat/mp"
    plugin_version = "1.0.0"
    plugin_description = "微信公众号插件，支持模板消息、客服消息、用户管理等"
    plugin_author = "三金的小虾米"
    
    # 客户端缓存
    _clients = {}
    
    def _get_client(self, app_id: str, app_secret: str):
        """获取公众号客户端"""
        key = f"{app_id}_{app_secret}"
        if key not in self._clients:
            self._clients[key] = WeChatClient(app_id, app_secret, session=MemoryStorage())
        return self._clients[key]
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行公众号操作
        
        Args:
            params:
                action: 操作类型
                    - send_template: 发送模板消息
                    - send_custom_message: 发送客服消息
                    - get_user_info: 获取用户信息
                    - get_user_list: 获取关注用户列表
                    - create_menu: 创建自定义菜单
                    - get_menu: 获取自定义菜单
                    - delete_menu: 删除自定义菜单
                app_id: 公众号AppID（必填）
                app_secret: 公众号AppSecret（必填）
                openid: 用户openid（发送消息、获取用户信息时必填）
                template_id: 模板ID（发送模板消息时必填）
                data: 模板数据（发送模板消息时必填）
                url: 跳转URL（模板消息可选）
                content: 消息内容（发送客服消息时必填）
                menus: 菜单配置（创建菜单时必填）
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
                url = params.get('url')
                mini_program = params.get('mini_program')
                
                if not openid or not template_id:
                    return {'success': False, 'error': '缺少openid或template_id参数'}
                
                result = client.message.send_template(
                    openid,
                    template_id,
                    data=data,
                    url=url,
                    mini_program=mini_program
                )
                return {'success': True, 'result': '模板消息发送成功', 'msg_id': result['msgid']}
            
            elif action == 'send_custom_message':
                openid = params.get('openid')
                content = params.get('content')
                msg_type = params.get('msg_type', 'text')
                
                if not openid or not content:
                    return {'success': False, 'error': '缺少openid或content参数'}
                
                if msg_type == 'text':
                    result = client.message.send_text(openid, content)
                elif msg_type == 'image':
                    # 先上传图片
                    media_result = client.media.upload('image', open(content, 'rb'))
                    media_id = media_result['media_id']
                    result = client.message.send_image(openid, media_id)
                else:
                    return {'success': False, 'error': f'不支持的消息类型: {msg_type}'}
                
                return {'success': True, 'result': '客服消息发送成功', 'response': result}
            
            elif action == 'get_user_info':
                openid = params.get('openid')
                lang = params.get('lang', 'zh_CN')
                if not openid:
                    return {'success': False, 'error': '缺少openid参数'}
                
                user_info = client.user.get(openid, lang=lang)
                return {'success': True, 'user_info': user_info}
            
            elif action == 'get_user_list':
                next_openid = params.get('next_openid', '')
                result = client.user.get(next_openid)
                return {
                    'success': True,
                    'total': result['total'],
                    'count': result['count'],
                    'openids': result['data']['openid'],
                    'next_openid': result['next_openid']
                }
            
            elif action == 'create_menu':
                menus = params.get('menus')
                if not menus or not isinstance(menus, dict):
                    return {'success': False, 'error': 'menus参数应为菜单配置字典'}
                
                result = client.menu.create(menus)
                return {'success': True, 'result': '菜单创建成功', 'response': result}
            
            elif action == 'get_menu':
                menu_info = client.menu.get()
                return {'success': True, 'menu': menu_info}
            
            elif action == 'delete_menu':
                client.menu.delete()
                return {'success': True, 'result': '菜单删除成功'}
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
        
        except Exception as e:
            return {'success': False, 'error': f'公众号操作失败: {str(e)}'}
