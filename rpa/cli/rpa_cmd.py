import click
import yaml
import json
from pathlib import Path
from typing import Optional

from rpa.core.flow import load_flow, Flow
from rpa.core.engine import execution_engine
from rpa.core.plugin import list_plugins


@click.group(name='rpa', help='RPA机器人流程自动化工具')
def rpa_cmd():
    pass


@rpa_cmd.command(help='执行流程')
@click.argument('flow_file')
@click.option('-c', '--context', help='上下文JSON字符串')
@click.option('-o', '--output', help='结果输出文件路径')
def run(flow_file: str, context: Optional[str] = None, output: Optional[str] = None):
    """执行流程"""
    try:
        # 解析上下文
        ctx = {}
        if context:
            ctx = json.loads(context)
        
        # 加载并执行流程
        flow = load_flow(flow_file)
        click.echo(f"开始执行流程：{flow.name} v{flow.version}")
        
        result = execution_engine.execute_flow(flow, context=ctx)
        
        if result['status'] == 'success':
            click.secho(f"✅ 流程执行成功！耗时：{result['duration']:.2f}秒", fg='green')
            for step in result['steps']:
                status = "✅" if step['status'] == 'success' else "❌"
                click.echo(f"  {status} {step['name']} - {step['duration']:.2f}s")
            
            # 输出结果
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                click.echo(f"结果已保存到：{output}")
        else:
            click.secho(f"❌ 流程执行失败：{result.get('error', '未知错误')}", fg='red')
    
    except Exception as e:
        click.secho(f"执行异常：{str(e)}", fg='red')
        exit(1)


@rpa_cmd.command(help='验证流程格式')
@click.argument('flow_file')
def validate(flow_file: str):
    """验证流程格式是否正确"""
    try:
        with open(flow_file, 'r', encoding='utf-8') as f:
            if flow_file.endswith('.json'):
                data = json.load(f)
            else:
                data = yaml.safe_load(f)
        
        flow = Flow(data)
        click.secho("✅ 流程格式验证通过！", fg='green')
    
    except Exception as e:
        click.secho(f"❌ 格式错误：{str(e)}", fg='red')
        exit(1)


@rpa_cmd.command(help='列出本地流程')
@click.option('-p', '--path', default='.', help='流程目录路径')
def list(path: str):
    """列出本地流程文件"""
    dir_path = Path(path)
    yaml_files = list(dir_path.glob("*.yaml")) + list(dir_path.glob("*.yml")) + list(dir_path.glob("*.json"))
    
    if not yaml_files:
        click.echo("未找到流程文件")
        return
    
    click.echo(f"找到 {len(yaml_files)} 个流程文件：")
    for f in yaml_files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                if f.suffix == '.json':
                    data = json.load(file)
                else:
                    data = yaml.safe_load(file)
                name = data.get('name', f.stem)
                version = data.get('version', '1.0.0')
                click.echo(f"  - {name} (v{version}) - {f.name}")
        except:
            click.echo(f"  - {f.name} (读取失败)")


@rpa_cmd.command(help='创建新流程模板')
@click.argument('name')
@click.option('-d', '--description', default='', help='流程描述')
@click.option('-t', '--template', default='empty', help='使用的模板')
def init(name: str, description: str = '', template: str = 'empty'):
    """创建新流程模板"""
    file_name = f"{name.replace(' ', '_')}.yaml"
    
    # 模板内容
    if template == 'empty':
        content = f"""# RPA流程定义
name: {name}
description: "{description}"
version: 1.0.0

trigger:
  type: manual

variables:
  # 全局变量
  app_id: "cli_xxxxxx"
  app_secret: "xxxxxx"

steps:
  - name: 示例步骤
    uses: feishu/bitable@1.0.0
    with:
      action: list_tables
      app_token: "xxxxxx"
      app_id: "${{ globals.app_id }}"
"""
    else:
        # 从模板目录加载
        template_path = Path(__file__).parent.parent / 'templates' / f"{template}.yaml"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = f"""# RPA流程定义
name: {name}
description: "{description}"
version: 1.0.0
"""
    
    # 保存文件
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    click.secho(f"✅ 流程模板已创建：{file_name}", fg='green')


@rpa_cmd.group(help='插件管理')
def plugin():
    pass


@plugin.command(name='list', help='列出所有已安装插件')
def list_plugins_cmd():
    """列出所有已安装插件"""
    plugins = list_plugins()
    if not plugins:
        click.echo("未安装任何插件")
        return
    
    click.echo(f"已安装 {len(plugins)} 个插件：")
    for p in plugins:
        click.echo(f"  - {p['name']} v{p['version']} - {p['description']} (作者：{p['author']})")


@rpa_cmd.command(help='启动Web控制台')
@click.option('-h', '--host', default='0.0.0.0', help='监听地址')
@click.option('-p', '--port', default=8888, help='监听端口')
@click.option('-d', '--debug', is_flag=True, help='调试模式')
def web(host: str = '0.0.0.0', port: int = 8888, debug: bool = False):
    """启动Web控制台"""
    try:
        from rpa.web.app import main
        click.echo(f"🌐 启动Web控制台，监听地址：http://{host}:{port}")
        click.echo(f"💡 打开浏览器访问上面的地址即可使用Web界面")
        main(host=host, port=port, debug=debug)
    except ImportError as e:
        click.secho(f"❌ 启动失败，缺少依赖：{str(e)}", fg='red')
        click.echo("请先安装Web依赖：pip install flask flask-cors flask-socketio")
        exit(1)
