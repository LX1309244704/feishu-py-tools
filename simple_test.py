# 简单测试
print("测试开始...")

# 测试1
print("测试 schemas...")
try:
    import rpa.schemas
    print("✅ schemas模块可导入")
except:
    print(f"❌ schemas模块导入失败: {e}")

# 测试2
print("\n测试 flow.py...")
try:
    import rpa.core.flow
    print("✅ flow.py 可导入")
except:
    print(f"❌ flow.py 导入失败: {e}")

# 测试3
print("\n测试 flow模块...")
try:
    from rpa.core import flow
    print("✅ flow 模块可导入")
except:
    print(f"❌ flow 模块导入失败: {e}")

# 测试4
print("\n测试 plugin...")
try:
    import rpa.plugins.feishu_plugins
    print("✅ feishu插件可导入")
except:
    print(f"❌ feishu插件导入失败: {e}")

# 测试5
print("\n测试 all plugins...")
try:
    from rpa.plugins import *
    print("✅ 所有插件可导入")
except:
    print(f"❌ 插件导入失败: {e}")

# 测试6
print("\n测试 GUI模块...")
try:
    import rpa.gui.main
    print("✅ GUI主模块可导入")
except:
    print(f"❌ GUI主模块导入失败: {e}")

print("\n✅ 测试完成！")
