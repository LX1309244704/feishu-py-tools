"""
RPA Web控制台后端
基于Flask实现
"""
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import yaml
import json
from pathlib import Path
from datetime import datetime
import subprocess
import threading
from typing import Dict, List

# 导入RPA核心
from rpa.core.flow import load_flow
from rpa.core.engine import execution_engine
from rpa.core.plugin import list_plugins

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
CORS(app)

# 全局配置
APP_ROOT = Path(__file__).parent.parent.parent
FLOWS_DIR = APP_ROOT / 'flows'  # 流程保存目录
FLOWS_DIR.mkdir(exist_ok=True)
EXECUTION_LOGS = []  # 执行日志内存存储，生产环境可以用数据库


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


# ==================== API接口 ====================
@app.route('/api/dashboard/stats')
def get_stats():
    """获取仪表盘统计"""
    flow_files = list(FLOWS_DIR.glob('*.yaml')) + list(FLOWS_DIR.glob('*.yml')) + list(FLOWS_DIR.glob('*.json'))
    total_flows = len(flow_files)
    
    # 统计执行数据
    today = datetime.now().strftime('%Y-%m-%d')
    today_executions = [log for log in EXECUTION_LOGS if log['start_time'].startswith(today)]
    today_count = len(today_executions)
    success_count = sum(1 for log in today_executions if log['status'] == 'success')
    success_rate = f"{(success_count / today_count * 100):.1f}%" if today_count > 0 else "0%"
    
    # 平均耗时
    total_duration = sum(log.get('duration', 0) for log in today_executions if log['status'] == 'success')
    avg_duration = f"{total_duration / max(success_count, 1):.2f}s"
    
    return jsonify({
        'success': True,
        'data': {
            'total_flows': total_flows,
            'today_executions': today_count,
            'success_rate': success_rate,
            'avg_duration': avg_duration
        }
    })


@app.route('/api/dashboard/recent_executions')
def get_recent_executions():
    """获取最近执行记录"""
    recent = sorted(EXECUTION_LOGS, key=lambda x: x['start_time'], reverse=True)[:10]
    return jsonify({
        'success': True,
        'data': recent
    })


@app.route('/api/flows')
def get_flows():
    """获取流程列表"""
    flow_files = list(FLOWS_DIR.glob('*.yaml')) + list(FLOWS_DIR.glob('*.yml')) + list(FLOWS_DIR.glob('*.json'))
    flows = []
    
    for f in flow_files:
        try:
            stat = f.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # 读取基础信息
            with open(f, 'r', encoding='utf-8') as file:
                if f.suffix == '.json':
                    data = json.load(file)
                else:
                    data = yaml.safe_load(file)
            
            flows.append({
                'name': data.get('name', f.stem),
                'description': data.get('description', ''),
                'version': data.get('version', '1.0.0'),
                'file_name': f.name,
                'path': str(f),
                'modified_time': mtime,
                'size': stat.st_size
            })
        except Exception as e:
            flows.append({
                'name': f.stem,
                'description': '读取失败',
                'file_name': f.name,
                'path': str(f),
                'modified_time': mtime,
                'error': str(e)
            })
    
    return jsonify({
        'success': True,
        'data': flows
    })


@app.route('/api/flow/<file_name>', methods=['GET'])
def get_flow(file_name):
    """获取流程内容"""
    try:
        file_path = FLOWS_DIR / file_name
        if not file_path.exists():
            return jsonify({'success': False, 'error': '流程不存在'}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'data': {
                'file_name': file_name,
                'content': content
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/flow', methods=['POST'])
def save_flow():
    """保存流程"""
    try:
        data = request.get_json()
        file_name = data.get('file_name')
        content = data.get('content')
        
        if not file_name or not content:
            return jsonify({'success': False, 'error': '缺少参数'}), 400
        
        file_path = FLOWS_DIR / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({'success': True, 'message': '保存成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/flow/delete', methods=['POST'])
def delete_flow():
    """删除流程"""
    try:
        data = request.get_json()
        file_name = data.get('file_name')
        
        if not file_name:
            return jsonify({'success': False, 'error': '缺少参数'}), 400
        
        file_path = FLOWS_DIR / file_name
        if not file_path.exists():
            return jsonify({'success': False, 'error': '流程不存在'}), 404
        
        file_path.unlink()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/flow/run', methods=['POST'])
def run_flow():
    """执行流程"""
    try:
        data = request.get_json()
        file_name = data.get('file_name')
        context = data.get('context', {})
        
        if not file_name:
            return jsonify({'success': False, 'error': '缺少file_name参数'}), 400
        
        file_path = FLOWS_DIR / file_name
        if not file_path.exists():
            return jsonify({'success': False, 'error': '流程不存在'}), 404
        
        # 加载流程
        flow = load_flow(str(file_path))
        
        # 异步执行
        execution_id = f"exec_{int(datetime.now().timestamp())}"
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        def execute_background():
            try:
                result = execution_engine.execute_flow(flow, context=context)
                log_entry = {
                    'execution_id': execution_id,
                    'flow_name': flow.name,
                    'file_name': file_name,
                    'start_time': start_time,
                    'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'duration': result.get('duration', 0),
                    'status': result['status'],
                    'error': result.get('error', ''),
                    'steps': result.get('steps', [])
                }
                EXECUTION_LOGS.append(log_entry)
                # 限制日志数量
                if len(EXECUTION_LOGS) > 1000:
                    EXECUTION_LOGS.pop(0)
            except Exception as e:
                log_entry = {
                    'execution_id': execution_id,
                    'flow_name': flow.name,
                    'file_name': file_name,
                    'start_time': start_time,
                    'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'failed',
                    'error': str(e)
                }
                EXECUTION_LOGS.append(log_entry)
        
        threading.Thread(target=execute_background, daemon=True).start()
        
        return jsonify({
            'success': True,
            'execution_id': execution_id,
            'message': '流程已开始执行'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/executions')
def get_executions():
    """获取执行记录"""
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    sorted_logs = sorted(EXECUTION_LOGS, key=lambda x: x['start_time'], reverse=True)
    total = len(sorted_logs)
    start = (page - 1) * page_size
    end = start + page_size
    data = sorted_logs[start:end]
    
    return jsonify({
        'success': True,
        'data': data,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@app.route('/api/templates')
def get_templates():
    """获取模板列表"""
    template_dir = APP_ROOT / 'rpa' / 'templates'
    template_files = list(template_dir.glob('*.yaml'))
    
    templates = []
    for f in template_files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            templates.append({
                'name': data.get('name', f.stem),
                'description': data.get('description', ''),
                'version': data.get('version', '1.0.0'),
                'file_name': f.name,
                'content': yaml.dump(data, allow_unicode=True, sort_keys=False)
            })
        except Exception as e:
            templates.append({
                'name': f.stem,
                'description': '读取失败',
                'file_name': f.name,
                'error': str(e)
            })
    
    return jsonify({
        'success': True,
        'data': templates
    })


@app.route('/api/plugins')
def get_plugins():
    """获取插件列表"""
    plugins = list_plugins()
    return jsonify({
        'success': True,
        'data': plugins
    })


@app.route('/api/validate', methods=['POST'])
def validate_flow():
    """验证流程格式"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        if not content:
            return jsonify({'success': False, 'error': '内容为空'}), 400
        
        # 尝试解析
        try:
            yaml_data = yaml.safe_load(content)
        except:
            try:
                yaml_data = json.loads(content)
            except:
                return jsonify({'success': False, 'error': '格式错误，不是有效的YAML/JSON'}), 400
        
        # 验证Flow
        from rpa.core.flow import Flow
        flow = Flow(yaml_data)
        
        return jsonify({'success': True, 'message': '格式验证通过'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# 静态文件
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


def main(host: str = '0.0.0.0', port: int = 8888, debug: bool = False):
    """启动Web控制台"""
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
