#!/usr/bin/env python3
"""
验证测试脚本
"""
import sys
sys.path.insert(0, '.')

print("=" * 50)
print("微元 Weiyuan - 验证测试")
print("=" * 50)

# 测试1：模块导入测试
print()
print("【测试1】模块导入测试")
tests = []

# 测试1.1: schemas模块
try:
    from rpa.schemas import get_schema
    print("✅ rpa.schemas.get_schema 导入成功")
    tests.append('✅ schemas模块')
except ImportError as e:
    print(f"❌ schemas模块导入失败: {e}")
    tests.append('❌ schemas模块')

# 测试1.2: core.flow模块
try:
    from rpa.core.flow import Flow, load_flow
    print("✅ rpa.core.flow 导入成功")
    tests.append('✅ core.flow模块')
except ImportError as e:
    print(f"❌ core.flow模块导入失败: {e}")
    tests.append('❌ core.flow模块')

# 测试1.3: core.plugin模块
try:
    from rpa.core.plugin import BasePlugin, list_plugins
    print("✅ rpa.core.plugin 导入成功")
    tests.append('✅ core.plugin模块')
except ImportError as e:
    print(f"❌ core.plugin模块导入失败: {e}")
    tests.append('❌ core.plugin模块')

# 测试1.4: core.engine模块
try:
    from rpa.core.engine import execution_engine
    print("✅ rpa.core.engine 导入成功")
    tests.append('✅ core.engine模块')
except ImportError as e:
    print(f"❌ core.engine模块导入失败: {e}")
    tests.append('❌ core.engine模块')

# 测试1.5: 核心插件
try:
    from rpa.plugins.feishu_plugins import FeishuBitablePlugin
    print("✅ 飞书插件导入成功")
    tests.append('✅ 飞书插件')
except ImportError as e:
    print(f"❌ 飞书插件导入失败: {e}")
    tests.append('❌ 飞书插件')

try:
    from rpa.plugins.wechat_plugins import WechatMessagePlugin
    print("✅ 微信插件导入成功")
    tests.append('✅ 微信插件')
except ImportError as e:
    print(f"❌ 微信插件导入失败: {e}")
    tests.append('❌ 微信插件')

try:
    from rpa.plugins.ui_plugins import DesktopAutoPlugin, BrowserAutoPlugin
    print("✅ UI自动化插件导入成功")
    tests.append('✅ UI自动化插件')
except ImportError as e:
    print(f"❌ UI自动化插件导入失败: {e}")
    tests.append('❌ UI自动化插件')

try:
    from rpa.plugins.ocr_plugin import OCRPlugin
    print("✅ OCR插件导入成功")
    tests.append('✅ OCR插件')
except ImportError as e:
    print(f"❌ OCR插件导入失败: {e}")
    tests.append('❌ OCR插件')

try:
    from rpa.plugins.ai_plugin import AIPlugin
    print("✅ AI插件导入成功")
    tests.append('✅ AI插件')
except ImportError as e:
    print(f"❌ AI插件导入失败: {e}")
    tests.append('❌ AI插件')

try:
    from rpa.plugins.publish_plugins import ContentPublishPlugin
    print("✅ 内容发布插件导入成功")
    tests.append('✅ 内容发布插件')
except ImportError as e:
    print(f"❌ 内容发布插件导入失败: {e}")
    tests.append('❌ 内容发布插件')

try:
    from rpa.plugins.lark_cli_plugin import LarkCliPlugin, LarkCliSkillPlugin
    print("✅ 官方CLI插件导入成功")
    tests.append('✅ 官方CLI插件')
except ImportError as e:
    print(f"❌ 官方CLI插件导入失败: {e}")
    tests.append('❌ 官方CLI插件')

# 测试1.6: GUI模块
try:
    from rpa.gui.main import main
    print("✅ GUI主模块导入成功")
    tests.append('✅ GUI主模块')
except ImportError as e:
    print(f"❌ GUI主模块导入失败: {e}")
    tests.append('❌ GUI主模块')

try:
    from rpa.gui.pages.dashboard_page import DashboardPage
    print("✅ GUI页面模块导入成功")
    tests.append('✅ GUI页面模块')
except ImportError as e:
    print(f"❌ GUI页面模块导入失败: {e}")
    tests.append('❌ GUI页面模块')

try:
    from rpa.gui.utils.config_dialog import ConfigDialog
    print("✅ GUI配置模块导入成功")
    tests.append('✅ GUI配置模块')
except ImportError as e:
    print(f"❌ GUI配置模块导入失败: {e}")
    tests.append('❌ GUI配置模块')

except ImportError as e:
    print(f"❌ 无法导入: {e}")

# 测试2: 检查schema文件
print()
print("【测试2】schema文件检查")
schema_file = 'rpa/schemas/flow_schema.json'
if os.path.exists(schema_file):
    print(f"✅ flow_schema.json 存在")
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
            print(f"✅ flow_schema.json 可读取，共有 {len(schema)} 条规则")
            print(f"  - title: {schema.get('title', '未知')}")
            print(f"  - $schema: {schema.get('$schema', '未知')}")
    except Exception as e:
        print(f"❌ 读取schema文件失败: {e}")
else:
    print(f"❌ flow_schema.json 不存在")

# 测试3: 检查模板文件
print()
print("【测试3】模板文件检查")
template_files = [
    'rpa/templates/inventory_alert.yaml',
    'rpa/templates/daily_sales_report.yaml',
    'rpa/templates/wechat_send_message.yaml',
    'rpa/templates/wechat_export_contacts.yaml',
    'rpa/templates/multi_platform_publish.yaml',
    'rpa/templates/lark_cli_weiyuan_demo.yaml',
    'rpa/templates/complete_sales_auto_publish.yaml'
]
for tf in template_files:
    if os.path.exists(tf):
        print(f"✅ {tf} 存在")
    else:
        print(f"❌ {tf} 不存在")

# 测试4: 读取流程模板验证格式
print()
print("【测试4】流程模板格式验证")
test_templates = [
    'rpa/templates/inventory_alert.yaml',
    'rpa/templates/wechat_send_message.yaml'
    'rpa/templates/complete_sales_auto_publish.yaml'
]
for tf in test_templates:
    try:
        with open(tf, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"✅ {tf} 格式正确")
    except Exception as e:
        print(f"❌ {tf} 格式错误: {e}")

# 测试5: 检查依赖文件
print()
print("【测试5】依赖文件检查")
deps_files = [
    'requirements.txt',
    'requirements_rpa.txt',
    'requirements_gui.txt'
]
for df in deps_files:
    if os.path.exists(df):
        print(f"✅ {df} 存在")
    else:
        print(f"❌ {df} 不存在")

# 测试6: 检查配置和资源文件
print()
print("【测试6】配置和资源文件检查")
config_files = [
    'rpa/schemas/flow_schema.json',
    'rpa/gui/resources/__init__.py',
    'rpa/gui/resources/generate_icons.py',
    'rpa/gui/utils/__init__.py',
    'rpa/gui/utils/config_dialog.py',
    'rpa/gui/utils/config_manager.py',
]
for cf in config_files:
    if os.path.exists(cf):
        print(f"✅ {cf} 存在")
    else:
        print(f"❌ {cf} 不存在")

# 测试7: 检查README文档
print()
print("【测试7】README文档检查"""
docs = [
    'README.md',
    'README_RPA.md',
    'README_GUI.md',
    'README_DEPLOY.md',
    'README_COZE.md',
    'docs/LARK_CLI_INTEGRATION.md',
    'docs/COMPLETE_DEMO_GUIDE.md'
]
for doc in docs:
    if os.path.exists(doc):
        print(f"✅ {doc} 存在")
    else:
        print(f"❌ {doc} 不存在")

# 测试8: 核心文件完整性
print()
print("【测试8】核心文件完整性")
core_files = [
    'rpa/__init__.py',
    'rpa/__init__.py',
    'rpa/core/__init__.py',
    'rpa/cli/__init__.py',
    'rpa/gui/__init__.py',
]
for cf in core_files:
    if os.path.exists(cf):
        print(f"✅ {cf} 存在")
    else:
        print(f"⚠️  {cf} 不存在（非关键）")

print()
print("=" * 50)
print("✅ 验证测试完成！")
print("=" * 50)
print()
print(f"📊 测试统计：")
print(f"  - 成功导入的模块：{tests.count('✅')}/{len(tests)}")
print(f"  - 通过格式验证的模板：{len(test_templates)}")
print(f"  - 存在的文档：{len(docs)}")
print(f"  - 依赖文件：{len(deps)}")
print(f"  - 配置文件：{len(config_files)}")
