"""
Flask Web应用
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from typing import Dict, Any, List, Optional


class WebApp:
    """Web应用类"""
    
    def __init__(self, import_name: str = "feishu_tools"):
        """
        初始化Web应用
        
        Args:
            import_name: 应用名称
        """
        self.app = Flask(import_name, 
                       template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                       static_folder=os.path.join(os.path.dirname(__file__), 'static'))
        
        # 配置CORS
        CORS(self.app)
        
        # 配置密钥
        self.app.config['SECRET_KEY'] = 'your-secret-key-here'
        self.app.config['JSON_AS_ASCII'] = False
        
        # 注册路由
        self._register_routes()
    
    def _register_routes(self):
        """注册路由"""
        
        # 首页
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        # API路由
        @self.app.route('/api/config', methods=['GET', 'POST'])
        def api_config():
            from feishu_cli.config import ConfigManager
            config = ConfigManager()
            
            if request.method == 'POST':
                data = request.json
                for key, value in data.items():
                    config.set(key, value)
                return jsonify({"success": True, "message": "配置已更新"})
            else:
                return jsonify(config.config)
        
        # 多维表格API
        @self.app.route('/api/bitable/tables', methods=['GET'])
        def api_bitable_tables():
            from feishu_core.bitable_manager import BitableManager
            manager = BitableManager(
                app_id=request.args.get('app_id'),
                app_secret=request.args.get('app_secret')
            )
            tables = manager.list_tables(request.args.get('app_token'))
            return jsonify(tables)
        
        @self.app.route('/api/bitable/records', methods=['GET', 'POST'])
        def api_bitable_records():
            from feishu_core.bitable_manager import BitableManager
            manager = BitableManager(
                app_id=request.args.get('app_id'),
                app_secret=request.args.get('app_secret')
            )
            
            if request.method == 'GET':
                records = manager.list_records(
                    app_token=request.args.get('app_token'),
                    table_id=request.args.get('table_id'),
                    page_size=int(request.args.get('page_size', 100))
                )
                return jsonify(records)
            
            elif request.method == 'POST':
                data = request.json
                record_id = manager.create_record(
                    app_token=data.get('app_token'),
                    table_id=data.get('table_id'),
                    fields=data.get('fields')
                )
                return jsonify({"success": True, "record_id": record_id})
        
        # 文档API
        @self.app.route('/api/doc/documents', methods=['GET', 'POST'])
        def api_doc_documents():
            from feishu_core.doc_manager import DocManager
            manager = DocManager(
                app_id=request.args.get('app_id'),
                app_secret=request.args.get('app_secret')
            )
            
            if request.method == 'GET':
                docs = manager.list_documents(request.args.get('folder_token'))
                return jsonify(docs)
            
            elif request.method == 'POST':
                data = request.json
                doc_id = manager.create_document(
                    title=data.get('title'),
                    content=data.get('content', ''),
                    folder_token=data.get('folder_token')
                )
                return jsonify({"success": True, "doc_id": doc_id})
        
        # 日历API
        @self.app.route('/api/calendar/events', methods=['GET', 'POST'])
        def api_calendar_events():
            from feeshu_core.calendar_manager import CalendarManager
            manager = CalendarManager(
                app_id=request.args.get('app_id'),
                app_secret=request.args.get('app_secret')
            )
            
            if request.method == 'GET':
                events = manager.list_events(
                    calendar_id=request.args.get('calendar_id'),
                    start_time=request.args.get('start_time'),
                    end_time=request.args.get('end_time')
                )
                return jsonify(events)
            
            elif request.method == 'POST':
                data = request.json
                event_id = manager.create_event(
                    calendar_id=data.get('calendar_id'),
                    title=data.get('title'),
                    start_time=data.get('start_time'),
                    end_time=data.get('end_time'),
                    description=data.get('description', ''),
                    attendees=data.get('attendees', [])
                )
                return jsonify({"success": True, "event_id": event_id})
        
        # 任务API
        @self.app.route('/api/task/tasks', methods=['GET', 'POST'])
        def api_task_tasks():
            from feishu_core.task_manager import TaskManager
            manager = TaskManager(
                app_id=request.args.get('app_id'),
                app_secret=request.get('app_secret')
            )
            
            if request.method == 'GET':
                tasks = manager.list_tasks(
                    tasklist_guid=request.args.get('tasklist_guid')
                )
                return jsonify(tasks)
            
            elif request.method == 'POST':
                data = request.json
                task_id = manager.create_task(
                    tasklist_guid=data.get('tasklist_guid'),
                    summary=data.get('summary'),
                    description=data.get('description', ''),
                    due_time=data.get('due_time'),
                    assignee=data.get('assignee')
                )
                return jsonify({"success": True, "task_id": task_id})
        
        # 消息API
        @self.app.route('/api/message/send', methods=['POST'])
        def api_message_send():
            from feishu_core.message_manager import MessageManager
            manager = MessageManager(
                app_id=request.args.get('app_id'),
                app_secret=request.get('app_secret')
            )
            
            data = request.json
            msg_id = manager.send_text_message(
                receive_id=data.get('receive_id'),
                content=data.get('content'),
                receive_id_type=data.get('receive_id_type', 'open_id')
            )
            return jsonify({"success": True, "message_id": msg_id})
        
        # AI查询API
        @self.app.route('/api/ai/query', methods=['POST'])
        def api_ai_query():
            from ai_integration.nl_query_processor import NLQueryProcessor
            from ai_integration.claude_model import ClaudeModel
            
            claude = ClaudeModel(api_key=request.args.get('claude_key'))
            processor = NLQueryProcessor(claude)
            
            data = request.json
            result = processor.process_query(
                query=data.get('query'),
                context=data.get('context')
            )
            return jsonify(result)
        
        # 数据清洗API
        @app.route('/ai/clean', methods=['POST'])
        def api_ai_clean():
            from ai_integration.data_cleaner import DataCleaner
            from ai_integration.claude_model import ClaudeModel
            
            claude = ClaudeModel(api_key=request.args.get('claude_key'))
            cleaner = DataCleaner(claude)
            
            data = request.json
            import pandas as pd
            from io import StringIO
            import json
            
            # 从JSON数据创建DataFrame
            df = pd.DataFrame(data.get('data'))
            
            if data.get('rules'):
                cleaned_df = cleaner.clean_dataframe(df, rules=data['rules'])
            else:
                cleaned_df = cleaner.clean_dataframe(df)
            
            # 返回清洗后的数据
            result = cleaned_df.to_dict('records')
            return jsonify({
                "success": True,
                "data": result,
                "stats": {
                    "original_rows": len(df),
                    "cleaned_rows": len(cleaned_df),
                    "removed_rows": len(df) - len(cleaned_df)
                }
            })
        
        # 健康检查
        @self.app.route('/health')
        def health():
            return jsonify({
                "status": "healthy",
                "version": "v2.0.0",
                "features": [
                    "多维表格",
                    "文档",
                    "日历",
                    "任务",
                    "消息",
                    "AI集成",
                    "数据清洗"
                ]
            })
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """
        运行Web应用
        
        Args:
            host: 主机地址
            port: 端口号
            debug: 调试模式
        """
        print(f"🚀 启动飞书Python工具箱Web界面...")
        print(f"📱 访问地址: http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)
