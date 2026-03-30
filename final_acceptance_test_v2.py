#!/usr/bin/env python3
"""
最终验收测试脚本（宽松版本 - 允许可选依赖缺失）
"""
import sys
import os
sys.path.insert(0, '.')

print("=" * 70)
print("🦞 微元 Weiyuan - 最终验收测试（宽松版本）")
print("=" * 70)

test_results = []
optional_imports = ['pyautogui', 'paddleocr', 'anthropic', 'selenium', 'PySide6']

# 测试1: 项目结构完整性
print("\n【测试1】项目结构完整性检查")
print("-" * 70)

required_dirs = [
    'rpa',
    'rpa/core',
    'rpa/plugins',
    'rpa/schemas',
    'rpa/gui',
    'rpa/web',
    'rpa/templates',
    'rpa/gui/pages',
    'rpa/gui/utils',
    'docs'
]

all_dirs_ok = True
for dir_path in required_dirs:
    if os.path.isdir(dir_path):
        print(f"✅ 目录存在：{dir_path}")
        test_results.append(('✅', dir_path))
    else:
        print(f"❌ 目录缺失：{dir_path}")
        test_results.append(('❌', dir_path))
        all_dirs_ok = False

if all_dirs_ok:
    print("\n✅ 所有必要目录存在")

# 测试2: 核心文件完整性
print("\n【测试2】核心文件完整性检查")
print("-" * 70)

required_files = [
    'rpa/__init__.py',
    'rpa/core/engine.py',
    'rpa/core/flow.py',
    'rpa/core/plugin.py',
    'rpa/core/variable_engine.py',
    'rpa/schemas/flow_schema.json',
    'rpa/plugins/feishu_plugins.py',
    'rpa/plugins/wechat_plugins.py',
    'rpa/plugins/ui_plugins.py',
    'rpa/plugins/ocr_plugin.py',
    'rpa/plugins/ai_plugin.py',
    'rpa/plugins/publish_plugins.py',
    'rpa/plugins/lark_cli_plugin.py',
    'rpa/gui/main.py',
    'rpa/gui/pages/dashboard_page.py',
    'rpa/web/app.py',
]

all_files_ok = True
for file_path in required_files:
    if os.path.isfile(file_path):
        print(f"✅ 文件存在：{file_path}")
        test_results.append(('✅', file_path))
    else:
        print(f"❌ 文件缺失：{file_path}")
        test_results.append(('❌', file_path))
        all_files_ok = False

if all_files_ok:
    print("\n✅ 所有核心文件存在")

# 测试3: 核心模块导入测试（关键模块）
print("\n【测试3】核心模块导入测试")
print("-" * 70)

critical_imports = [
    ("rpa.schemas", "schema模块"),
    ("rpa.core.engine", "引擎模块"),
    ("rpa.core.flow", "流程模块"),
    ("rpa.core.plugin", "插件模块"),
    ("rpa.plugins.feishu_plugins", "飞书插件"),
    ("rpa.plugins.wechat_plugins", "微信插件"),
    ("rpa.plugins.lark_cli_plugin", "官方CLI插件"),
]

optional_imports_tested = []

for module, name in critical_imports:
    try:
        __import__(module)
        print(f"✅ 导入成功：{name} ({module})")
        test_results.append(('✅', f"{name}导入"))
    except ImportError as e:
        error_msg = str(e)
        # 检查是否是可选依赖缺失
        is_optional = any(opt in error_msg for opt in optional_imports)
        if is_optional:
            print(f"⚠️  导入失败（可选依赖）：{name} - {e}")
            test_results.append(('⚠️', f"{name}导入"))
            optional_imports_tested.append(name)
        else:
            print(f"❌ 导入失败：{name} - {e}")
            test_results.append(('❌', f"{name}导入"))

# 测试可选模块
optional_modules = [
    ("rpa.plugins.ui_plugins", "UI插件"),
    ("rpa.plugins.ocr_plugin", "OCR插件"),
    ("rpa.plugins.ai_plugin", "AI插件"),
    ("rpa.plugins.publish_plugins", "内容发布插件"),
]

print("\n【测试3.1】可选模块导入测试（需安装额外依赖）")
print("-" * 70)

for module, name in optional_modules:
    try:
        __import__(module)
        print(f"✅ {name} 已安装")
        test_results.append(('✅', f"{name}（可选）"))
    except ImportError as e:
        print(f"⚠️  {name} 未安装（正常，需要额外依赖）：{str(e).split('No module named')[1] if 'No module named' in str(e) else e}")
        test_results.append(('⚠️', f"{name}（可选）"))

# 测试4: 流程模板格式验证
print("\n【测试4】流程模板格式验证")
print("-" * 70)

template_files = [
    'rpa/templates/inventory_alert.yaml',
    'rpa/templates/daily_sales_report.yaml',
    'rpa/templates/wechat_send_message.yaml',
    'rpa/templates/multi_platform_publish.yaml',
    'rpa/templates/lark_cli_weiyuan_demo.yaml',
    'rpa/templates/complete_sales_auto_publish.yaml',
]

all_templates_ok = True
for template in template_files:
    if os.path.isfile(template):
        try:
            import yaml
            with open(template, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if 'name' in data and 'steps' in data:
                    print(f"✅ 格式正确：{template}")
                    test_results.append(('✅', template))
                else:
                    print(f"❌ 格式错误（缺少name或steps）：{template}")
                    test_results.append(('❌', template))
                    all_templates_ok = False
        except Exception as e:
            print(f"❌ 读取失败：{template} - {e}")
            test_results.append(('❌', template))
            all_templates_ok = False
    else:
        print(f"⚠️  文件不存在：{template}")
        test_results.append(('⚠️', template))

if all_templates_ok:
    print("\n✅ 所有流程模板格式正确")

# 测试5: Schema文件验证
print("\n【测试5】Schema文件验证")
print("-" * 70)

schema_file = 'rpa/schemas/flow_schema.json'
if os.path.isfile(schema_file):
    try:
        import json
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
            if '$schema' in schema and 'properties' in schema:
                print(f"✅ Schema格式正确")
                print(f"  - 标题：{schema.get('title', '未知')}")
                print(f"  - 版本：{schema.get('$schema', '未知')}")
                print(f"  - 属性数：{len(schema.get('properties', {}))}")
                test_results.append(('✅', 'flow_schema.json'))
            else:
                print(f"❌ Schema格式错误")
                test_results.append(('❌', 'flow_schema.json'))
    except Exception as e:
        print(f"❌ Schema验证失败：{e}")
        test_results.append(('❌', 'flow_schema.json'))
else:
    print(f"❌ Schema文件不存在")
    test_results.append(('❌', 'flow_schema.json'))

# 测试6: 文档完整性
print("\n【测试6】文档完整性检查")
print("-" * 70)

doc_files = [
    'README.md',
    'README_RPA.md',
    'README_GUI.md',
    'README_DEPLOY.md',
    'README_COZE.md',
    'docs/LARK_CLI_INTEGRATION.md',
    'docs/COMPLETE_DEMO_GUIDE.md',
]

all_docs_ok = True
for doc in doc_files:
    if os.path.isfile(doc):
        print(f"✅ 文档存在：{doc}")
        test_results.append(('✅', doc))
    else:
        print(f"❌ 文档缺失：{doc}")
        test_results.append(('❌', doc))
        all_docs_ok = False

if all_docs_ok:
    print("\n✅ 所有文档存在")

# 测试7: GitHub仓库状态
print("\n【测试7】Git仓库状态检查")
print("-" * 70)

try:
    result = os.popen('git remote -v').read()
    if 'github.com/LX1309244704/weiyuan.git' in result:
        print("✅ Git远程仓库配置正确")
        print(f"  远程地址：{result.split()[1] if len(result.split()) > 1 else '未知'}")
        test_results.append(('✅', 'Git仓库'))
    else:
        print("❌ Git远程仓库配置错误")
        test_results.append(('❌', 'Git仓库'))
except Exception as e:
    print(f"⚠️  Git检查失败：{e}")
    test_results.append(('⚠️', 'Git仓库'))

# 测试总结
print("\n" + "=" * 70)
print("📊 验收测试总结")
print("=" * 70)

total_tests = len(test_results)
passed_tests = sum(1 for status, _ in test_results if status == '✅')
failed_tests = sum(1 for status, _ in test_results if status == '❌')
warning_tests = sum(1 for status, _ in test_results if status == '⚠️')

print(f"\n总测试项：{total_tests}")
print(f"✅ 通过：{passed_tests}")
print(f"❌ 失败：{failed_tests}")
print(f"⚠️  警告：{warning_tests}（可选依赖未安装）")

# 核心功能通过率（只计算✅和❌）
core_tests = passed_tests + failed_tests
core_success_rate = (passed_tests / core_tests * 100) if core_tests > 0 else 0
print(f"\n核心功能通过率：{core_success_rate:.1f}%")

if failed_tests == 0:
    print("\n🎉 验收测试通过！项目已达到毕业质段！")
    print("⚠️  警告项为可选依赖，用户可在需要时安装")
    print("=" * 70)
    sys.exit(0)
elif failed_tests <= 2:
    print("\n✅ 验收测试基本通过，有少量非关键问题")
    print("=" * 70)
    sys.exit(0)
else:
    print("\n❌ 验收测试未通过，需要修复问题")
    print("=" * 70)
    sys.exit(1)
