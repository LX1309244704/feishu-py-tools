#!/usr/bin/env python3
"""
逐步验证测试
"""
import sys
sys.path.insert(0, '.')

print("=" * 50)
print("逐步验证")
print("=" * 50)

# 测试1: schemas模块
print("测试1: rpa.schemas...")
try:
    from rpa.schemas import get_schema
    print("✅ rpa.schemas 模块导入成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")

# 测试2: flow模块
print("\n测试2: rpa.core.flow...")
try:
    from rpa.core.flow import Flow
    print("✅ rpa.core.flow 模块导入成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")

# 测试3: 所有核心插件
print("\n测试3: 核心插件...")
plugins_to_test = [
    ("feishu", "rpa.plugins.feishu_plugins", ["FeishuBitablePlugin", "FeishuMessagePlugin", "FeishuDocPlugin"]),
    ("wechat", "rpa.plugins.wechat_plugins", ["WechatMessagePlugin", "WechatWorkPlugin", "WechatMpPlugin"]),
    ("ui", "rpa.plugins.ui_plugins", ["DesktopAutoPlugin", "BrowserAutoPlugin"]),
    ("ocr", "rpa.plugins.ocr_plugin", ["OCRPlugin"]),
    ("ai", "rpa.plugins.ai_plugin", ["AIPlugin"]),
    ("publish", "rpa.plugins.publish_plugins", ["ContentPublishPlugin"]),
    ("lark_cli", "rpa.plugins.lark_cli_plugin", ["LarkCliPlugin", "LarkCliSkillPlugin"]),
]

for category, module_path, plugin_classes in plugins_to_test:
    print(f"\n测试4: {category}插件...")
    for plugin_class in plugin_classes:
        try:
            # 只检查导入，不实例化（避免参数问题）
            if 'class ' + plugin_class.__name__ in dir():
                print(f"  ✅ {plugin_class.__name__} 导入成功")
            else:
                print(f"  ❌ {plugin_class.__name__} 未找到")
        except Exception as e:
            print(f"  ❌ {plugin_class.__name__} 导入异常: {e}")

# 测试5: GUI模块
print("\n测试5: GUI模块...")
gui_modules = [
    ("main", "rpa.gui.main", ["RPAMainWindow", "get_icon", "get_config", "main"]),
    ("dashboard_page", "rpa/gui/pages/dashboard_page", ["DashboardPage"]),
    ("config_manager", "rpa/gui/utils/config_manager", ["ConfigManager", "get_config"]),
    ("config_dialog", "rpa/gui/utils/config_dialog", ["ConfigDialog"]),
]

for category, module_path, classes in gui_modules:
    print(f"\n测试6: {category}模块...")
    for class_name in classes:
        try:
            if 'class ' + class_name in dir():
                print(f"  ✅ {class_name} 导入成功")
            else:
                print(f"  ❌ {class_name} 未找到")
        except Exception as e:
            print(f"  ❌ {class_name} 导入异常: {e}")

print()
print("=" * 50)
print("✅ 逐步验证完成")
print("=" * 50)
