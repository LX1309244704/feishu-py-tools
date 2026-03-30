"""
RPA命令行入口
"""
import click
import json
from pathlib import Path
from tabulate import tabulate

from rpa.core.flow import load_flow
from rpa.core.engine import execution_engine
from rpa.core.plugin import list_plugins


@click.group(name='rpa')
def rpa_group():
    """RPA机器人流程自动化工具"""
    pass


@rpa_group.command()
@click.argument('flow_path')
@click.option('--context', '-c', help='上下文JSON字符串')
@click.option('--output', '-o', help='输出结果文件路径')
def run(flow_path, context, output):
    """执行RPA流程"""
    try:
        # 加载流程
        flow = load_flow(flow_path)
        click.echo(f"📋 加载流程: {flow.name} v{flow.version}")
        click.echo(f"📝 步骤数量: {len(flow.steps)}")
        
        # 解析上下文
        ctx = {}
        if context:
            ctx = json.loads(context)
        
        # 执行流程
        click.echo("\n🚀 开始执行流程...")
        result = execution_engine.execute_flow(flow, ctx)
        
        # 输出结果
        click.echo(f"\n✅ 执行完成! 状态: {result['status']}")
        click.echo(f"⏱️  耗时: {result['duration']:.2f}秒")
        
        if result['status'] == 'success':
            click.echo("\n📊 步骤执行情况:")
            for step in result['steps']:
                status_icon = "✅" if step['status'] == 'success' else "❌" if step['status'] == 'failed' else "⏭️"
                click.echo(f"  {status_icon} {step['name']} - {step['duration']:.2f}s")
        else:
            click.echo(f"\n❌ 错误信息: {result.get('error', '未知错误')}")
        
        # 保存输出
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            click.echo(f"\n💾 结果已保存到: {output}")
        
        return result
        
    except Exception as e:
        click.echo(f"\n❌ 执行失败: {str(e)}", err=True)
        raise SystemExit(1)


@rpa_group.command()
@click.argument('flow_path')
def validate(flow_path):
    """验证流程文件格式是否正确"""
    try:
        flow = load_flow(flow_path)
        click.echo(f"✅ 流程格式正确!")
        click.echo(f"  名称: {flow.name}")
        click.echo(f"  版本: {flow.version}")
        click.echo(f"  步骤: {len(flow.steps)}个")
        if flow.trigger:
            click.echo(f"  触发方式: {flow.trigger['type']}")
        return True
    except Exception as e:
        click.echo(f"❌ 流程格式错误: {str(e)}", err=True)
        return False


@rpa_group.command(name='list')
def list_flows():
    """列出当前目录下的所有RPA流程"""
    flow_files = list(Path('.').glob('*.yaml')) + list(Path('.').glob('*.yml')) + list(Path('.').glob('*.json'))
    flows = []
    
    for f in flow_files:
        try:
            flow = load_flow(str(f))
            flows.append({
                'name': flow.name,
                'file': f.name,
                'version': flow.version,
                'steps': len(flow.steps),
                'trigger': flow.trigger.get('type', 'manual'),
                'modified': flow.last_modified.strftime('%Y-%m-%d %H:%M')
            })
        except:
            pass
    
    if flows:
        click.echo("📋 可用RPA流程:")
        headers = ['名称', '文件', '版本', '步骤数', '触发方式', '修改时间']
        table = [[f['name'], f['file'], f['version'], f['steps'], f['trigger'], f['modified']] for f in flows]
        click.echo(tabulate(table, headers=headers, tablefmt='grid'))
    else:
        click.echo("ℹ️  当前目录下没有找到有效的RPA流程文件")


@rpa_group.group()
def plugin():
    """插件管理命令"""
    pass


@plugin.command(name='list')
def list_plugins_cmd():
    """列出所有已安装的插件"""
    plugins = list_plugins()
    
    if plugins:
        click.echo("🔌 已安装插件:")
        headers = ['名称', '版本', '描述', '作者']
        table = [[p['name'], p['version'], p['description'], p['author']] for p in plugins]
        click.echo(tabulate(table, headers=headers, tablefmt='grid'))
    else:
        click.echo("ℹ️  没有已安装的插件")


@rpa_group.command()
@click.argument('name')
@click.option('--description', '-d', help='流程描述')
def init(name, description):
    """初始化一个新的RPA流程模板"""
    template = f"""# RPA流程定义
name: {name}
description: "{description or '自动生成的RPA流程'}"
version: 1.0.0

# 触发条件
trigger:
  type: manual  # manual/schedule/webhook/event/condition
  # cron: "0 9 * * 1-5"  # schedule类型时填写，工作日9点执行
  # event: "new_record"  # event类型时填写

# 全局变量
variables:
  app_id: "cli_xxxxxx"
  app_secret: "xxxxxx"
  app_token: "xxxxxx"

# 流程步骤
steps:
  - name: 示例步骤
    uses: feishu/bitable@1.0.0
    with:
      action: list_tables
      app_token: "${{ globals.app_token }}"
      app_id: "${{ globals.app_id }}"
      app_secret: "${{ globals.app_secret }}"
    timeout: 300
    retry: 0
    continue_on_failure: false

# 执行成功后的回调步骤
on_success:
  - name: 成功通知
    uses: feishu/message@1.0.0
    with:
      receive_id: "ou_xxxxxx"
      content: "流程执行成功！"

# 执行失败后的回调步骤
on_failure:
  - name: 失败告警
    uses: feishu/message@1.0.0
    with:
      receive_id: "ou_xxxxxx"
      content: "流程执行失败！错误：${{ error }}"

# 流程设置
settings:
  log_level: info
  timeout: 3600
  max_parallel: 1
"""
    
    filename = f"{name.lower().replace(' ', '_')}.yaml"
    if Path(filename).exists():
        click.echo(f"❌ 文件已存在: {filename}", err=True)
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(template)
    
    click.echo(f"✅ 流程模板已创建: {filename}")
    click.echo("ℹ️  请编辑该文件配置流程逻辑，然后使用 opencli rpa run 执行")


# 加载插件（自动注册）
def load_plugins():
    """加载所有插件"""
    import importlib
    import os
    
    plugins_dir = Path(__file__).parent.parent / "plugins"
    for f in plugins_dir.glob("*.py"):
        if f.stem != '__init__':
            importlib.import_module(f"rpa.plugins.{f.stem}")


# 加载插件
load_plugins()

__all__ = ['rpa_group']
