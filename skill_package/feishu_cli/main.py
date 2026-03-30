#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weiyuan CLI 主入口
"""
import sys
import click
from rich.console import Console
from rich.table import Table
from pathlib import Path

# 初始化终端
console = Console()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """飞书Python工具箱 - 基于飞书CLI的Python增强版飞书管理工具"""
    pass


@cli.group()
def base():
    """多维表格管理"""
    pass


@base.command()
@click.option('--app-token', help='多维表格App Token')
@click.option('--table-id', help='表格ID')
def list(app_token=None, table_id=None):
    """列出多维表格或表格记录"""
    from feishu_core.base import BitableManager
    
    manager = BitableManager()
    
    if not app_token:
        # 列出所有表格
        tables = manager.list_tables()
        table = Table(title="多维表格列表")
        table.add_column("App Token", style="cyan")
        table.add_column("Table Name", style="green")
        table.add_column("Table ID", style="yellow")
        
        for t in tables:
            table.add_row(t['app_token'], t['name'], t['table_id'])
        
        console.print(table)
    else:
        # 列出表格记录
        records = manager.list_records(app_token, table_id)
        table = Table(title=f"表格记录 ({app_token})")
        
        # 添加列
        if records:
            for field in records[0].keys():
                table.add_column(field)
        
        for record in records:
            table.add_row(*record.values())
        
        console.print(table)


@base.command()
@click.option('--name', required=True, help='表格名称')
@click.option('--template', help='使用模板', type=click.Choice(['crm', 'project', 'task', 'asset']))
@click.option('--app-token', help='多维表格App Token（可选，不传则使用默认）')
def create(name, template=None, app_token=None):
    """创建多维表格"""
    from feishu_core.base import BitableManager
    
    manager = BitableManager()
    
    console.print(f"[cyan]正在创建表格: {name}[/cyan]")
    
    if template:
        table_id = manager.create_table_from_template(template, name=name, app_token=app_token)
        console.print(f"[green]✓ 使用模板 '{template}' 创建成功[/green]")
    else:
        table_id = manager.create_table(name, app_token=app_token)
        console.print(f"[green]✓ 创建成功[/green]")
    
    console.print(f"Table ID: {table_id}")


@base.command()
@click.option('--app-token', required=True, help='多维表格App Token')
@click.option('--table-id', required=True, help='表格ID')
@click.option('--file', required=True, type=click.Path(exists=True), help='CSV文件路径')
def import_data(app_token, table_id, file):
    """批量导入数据"""
    from feishu_core.base import BitableManager
    
    manager = BitableManager()
    
    console.print(f"[cyan]正在导入数据到表格 {table_id}...[/cyan]")
    
    count = manager.import_from_csv(app_token, table_id, str(file))
    
    console.print(f"[green]✓ 成功导入 {count} 条记录[/green]")


@base.command()
@click.option('--app-token', required=True, help='多维表格App Token')
@click.option('--table-id', required=True, help='表格ID')
@click.option('--format', type=click.Choice(['csv', 'json', 'xlsx']), default='csv', help='导出格式')
@click.option('--output', type=click.Path(), help='输出文件路径')
def export(app_token, table_id, format, output):
    """导出数据"""
    from feishu_core.base import BitableManager
    
    manager = BitableManager()
    
    console.print(f"[cyan]正在导出表格 {table_id} 的数据...[/cyan]")
    
    data = manager.export_data(app_token, table_id, format)
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(data)
        console.print(f"[green]✓ 数据已导出到: {output}[/green]")
    else:
        console.print(data)


@base.command()
@click.option('--app-token', required=True, help='多维表格App Token')
@click.option('--table-id', required=True, help='表格ID')
@click.option('--prompt', required=True, help='AI辅助录入提示词')
@click.option('--model', default='claude', help='AI模型')
def ai_fill(app_token, table_id, prompt, model):
    """AI辅助录入数据"""
    from ai_integration.processor import AIDataProcessor
    
    processor = AIDataProcessor(model=model)
    
    console.print(f"[cyan]正在使用 {model} 辅助录入数据...[/cyan]")
    console.print(f"提示词: {prompt}")
    
    count = processor.process_prompt(
        app_token=app_token,
        table_id=table_id,
        prompt=prompt
    )
    
    console.print(f"[green]✓ AI成功录入 {count} 条记录[/green]")


@cli.group()
def doc():
    """文档管理"""
    pass


@doc.command()
@click.option('--doc-id', help='文档ID')
def read(doc_id):
    """读取文档内容"""
    from feishu_core.doc import DocManager
    
    manager = DocManager()
    
    if not doc_id:
        console.print("[yellow]请提供文档ID[/yellow]")
        return
    
    content = manager.read_document(doc_id)
    
    console.print(f"[cyan]文档内容:[/cyan]")
    console.print(content)


@doc.command()
@click.option('--title', required=True, help='文档标题')
@click.option('--content', help='文档内容（Markdown格式）')
def create(title, content):
    """创建新文档"""
    from feishu_core.doc import DocManager
    
    manager = DocManager()
    
    console.print(f"[cyan]正在创建文档: {title}[/cyan]")
    
    doc_id = manager.create_document(title, content)
    
    console.print(f"[green]✓ 文档创建成功[/green]")
    console.print(f"Document ID: {doc_id}")


@cli.group()
def workflow():
    """工作流管理"""
    pass


@workflow.command()
@click.option('--config', type=click.Path(exists=True), help='工作流配置文件')
def run(config):
    """运行工作流"""
    from workflows.engine import WorkflowEngine
    
    engine = WorkflowEngine()
    
    console.print(f"[cyan]正在加载工作流配置: {config}[/cyan]")
    
    engine.load_config(str(config))
    engine.run()
    
    console.print("[green]✓ 工作流执行完成[/green]")


@workflow.command()
def list_workflows():
    """列出所有工作流"""
    from workflows.engine import WorkflowEngine
    
    engine = WorkflowEngine()
    workflows = engine.list_workflows()
    
    table = Table(title="工作流列表")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Status", style="yellow")
    
    for wf in workflows:
        table.add_row(wf['name'], wf['type'], wf['status'])
    
    console.print(table)


@cli.group()
def ai():
    """AI集成"""
    pass


@ai.command()
@click.option('--prompt', required=True, help='查询提示词')
@click.option('--app-token', help='多维表格App Token')
@click.option('--table-id', help='表格ID')
@click.option('--model', default='claude', help='AI模型')
def query(prompt, app_token, table_id, model):
    """自然语言查询"""
    from ai_integration.assistant import FeishuAssistant
    
    assistant = FeishuAssistant(model=model)
    
    console.print(f"[cyan]正在使用 {model} 查询...[/cyan]")
    console.print(f"查询: {prompt}")
    
    result = assistant.query(
        prompt=prompt,
        app_token=app_token,
        table_id=table_id
    )
    
    console.print("\n[cyan]查询结果:[/cyan]")
    console.print(result)


@ai.command()
@click.option('--scenario', help='应用场景')
def recommend(scenario):
    """智能推荐"""
    from ai_integration.assistant import FeishuAssistant
    
    assistant = FeishuAssistant()
    
    console.print(f"[cyan]正在分析场景: {scenario}[/cyan]")
    
    recommendations = assistant.recommend(scenario)
    
    console.print("\n[cyan]推荐方案:[/cyan]")
    for i, rec in enumerate(recommendations, 1):
        console.print(f"{i}. {rec}")


@cli.group()
def viz():
    """数据可视化"""
    pass


@viz.command()
@click.option('--app-token', required=True, help='多维表格App Token')
@click.option('--table-id', required=True, help='表格ID')
@click.option('--charts', help='图表类型（逗号分隔）')
def dashboard(app_token, table_id, charts):
    """生成仪表盘"""
    from visualization.dashboard import DashboardGenerator
    
    generator = DashboardGenerator()
    
    console.print(f"[cyan]正在生成仪表盘...[/cyan]")
    
    chart_list = charts.split(',') if charts else None
    
    output = generator.create_dashboard(
        app_token=app_token,
        table_id=table_id,
        charts=chart_list
    )
    
    console.print(f"[green]✓ 仪表盘生成成功[/green]")
    console.print(f"输出文件: {output}")


@cli.group()
def config():
    """配置管理"""
    pass


@config.command()
def init():
    """初始化配置"""
    from feishu_cli.config import ConfigManager
    
    manager = ConfigManager()
    
    console.print("[cyan]正在初始化配置...[/cyan]")
    
    manager.init_config()
    
    console.print("[green]✓ 配置初始化完成[/green]")
    console.print("[yellow]请运行以下命令完成授权:[/yellow]")
    console.print("  feishu-cli config auth")


@config.command()
def auth():
    """授权配置"""
    from feishu_cli.config import ConfigManager
    
    manager = ConfigManager()
    
    console.print("[cyan]正在生成授权链接...[/cyan]")
    
    auth_url = manager.get_auth_url()
    
    console.print(f"\n[yellow]请在浏览器中打开以下链接完成授权:[/yellow]")
    console.print(f"[blue]{auth_url}[/blue]")


def main():
    """主函数"""
    cli()


if __name__ == '__main__':
    main()
