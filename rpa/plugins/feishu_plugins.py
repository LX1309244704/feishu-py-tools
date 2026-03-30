"""
飞书多维表格插件
"""
from typing import Dict, Any
from rpa.core.plugin import BasePlugin, register_plugin
from feishu_core.bitable_manager import BitableManager


@register_plugin
class BitablePlugin(BasePlugin):
    """飞书多维表格插件"""
    
    plugin_name = "feishu/bitable"
    plugin_version = "1.0.0"
    plugin_description = "飞书多维表格操作：获取表格、记录、创建、更新、删除等"
    plugin_author = "三金的小虾米"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行多维表格操作
        
        Args:
            params: 参数，必须包含action
                action可选值：
                - list_tables: 获取表格列表
                - list_records: 获取记录列表
                - create_record: 创建记录
                - update_record: 更新记录
                - delete_record: 删除记录
                - import_csv: 导入CSV
                - export_csv: 导出CSV
        """
        action = params.get('action')
        if not action:
            return {'success': False, 'error': '缺少action参数'}
        
        app_id = params.get('app_id') or self.config.get('app_id')
        app_secret = params.get('app_secret') or self.config.get('app_secret')
        
        if not app_id or not app_secret:
            return {'success': False, 'error': '缺少app_id或app_secret参数'}
        
        try:
            manager = BitableManager(app_id=app_id, app_secret=app_secret)
            app_token = params['app_token']
            
            if action == 'list_tables':
                tables = manager.list_tables(app_token)
                return {'success': True, 'data': tables}
            
            elif action == 'list_records':
                table_id = params['table_id']
                page_size = params.get('page_size', 100)
                records = manager.list_records(app_token, table_id, page_size=page_size)
                return {'success': True, 'data': records}
            
            elif action == 'create_record':
                table_id = params['table_id']
                fields = params['fields']
                record_id = manager.create_record(app_token, table_id, fields)
                return {'success': True, 'record_id': record_id}
            
            elif action == 'update_record':
                table_id = params['table_id']
                record_id = params['record_id']
                fields = params['fields']
                manager.update_record(app_token, table_id, record_id, fields)
                return {'success': True}
            
            elif action == 'delete_record':
                table_id = params['table_id']
                record_id = params['record_id']
                manager.delete_record(app_token, table_id, record_id)
                return {'success': True}
            
            elif action == 'import_csv':
                table_id = params['table_id']
                csv_file = params['csv_file']
                count = manager.import_from_csv(app_token, table_id, csv_file)
                return {'success': True, 'import_count': count}
            
            elif action == 'export_csv':
                table_id = params['table_id']
                output_file = params.get('output_file', 'output.csv')
                file_path = manager.export_to_csv(app_token, table_id, output_file)
                return {'success': True, 'file_path': file_path}
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


@register_plugin
class MessagePlugin(BasePlugin):
    """飞书消息插件"""
    
    plugin_name = "feishu/message"
    plugin_version = "1.0.0"
    plugin_description = "飞书消息发送：文本、富文本、卡片、图片、文件等"
    plugin_author = "三金的小虾米"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送飞书消息
        
        Args:
            params: 参数
                receive_id: 接收人ID/群ID
                content: 消息内容
                msg_type: 消息类型，默认text
                receive_id_type: ID类型，默认open_id
        """
        from feishu_core.message_manager import MessageManager
        
        app_id = params.get('app_id') or self.config.get('app_id')
        app_secret = params.get('app_secret') or self.config.get('app_secret')
        
        if not app_id or not app_secret:
            return {'success': False, 'error': '缺少app_id或app_secret参数'}
        
        try:
            manager = MessageManager(app_id=app_id, app_secret=app_secret)
            receive_id = params['receive_id']
            content = params['content']
            msg_type = params.get('msg_type', 'text')
            receive_id_type = params.get('receive_id_type', 'open_id')
            
            msg_id = manager.send_text_message(
                receive_id=receive_id,
                content=content,
                receive_id_type=receive_id_type
            )
            
            return {'success': True, 'message_id': msg_id}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}


@register_plugin
class DocPlugin(BasePlugin):
    """飞书文档插件"""
    
    plugin_name = "feishu/doc"
    plugin_version = "1.0.0"
    plugin_description = "飞书文档操作：创建、读取、更新、导出等"
    plugin_author = "三金的小虾米"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        from feishu_core.doc_manager import DocManager
        
        app_id = params.get('app_id') or self.config.get('app_id')
        app_secret = params.get('app_secret') or self.config.get('app_secret')
        
        if not app_id or not app_secret:
            return {'success': False, 'error': '缺少app_id或app_secret参数'}
        
        try:
            manager = DocManager(app_id=app_id, app_secret=app_secret)
            action = params.get('action', 'get')
            
            if action == 'create':
                title = params['title']
                content = params.get('content', '')
                folder_token = params.get('folder_token')
                doc_id = manager.create_document(title, content, folder_token)
                return {'success': True, 'doc_id': doc_id}
            
            elif action == 'get':
                doc_id = params['doc_id']
                content = manager.get_document_content(doc_id)
                return {'success': True, 'content': content}
            
            elif action == 'update':
                doc_id = params['doc_id']
                content = params['content']
                mode = params.get('mode', 'append')  # append/overwrite
                manager.update_document(doc_id, content, mode)
                return {'success': True}
            
            elif action == 'export':
                doc_id = params['doc_id']
                output_file = params.get('output_file', 'doc.md')
                file_path = manager.export_document(doc_id, output_file)
                return {'success': True, 'file_path': file_path}
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
