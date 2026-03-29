# 🎉 FeiShu-Py-Tools v2.0.0 发布说明

## 📅 发布日期
2026-03-30

## 🎯 版本亮点
**飞书Python工具箱v2.0.0版本正式发布！** 本次更新带来了完整的工作流引擎、高级数据可视化和插件系统，大幅提升了工具的自动化能力和扩展性。

---

## ✨ 新增功能

### 1. 🚀 工作流引擎（Workflow Engine）

**模块位置**：`workflows/engine.py`
**代码行数**：约600行

#### 核心组件

##### 1.1 触发器系统（Trigger）
支持5种触发器类型：
- **定时触发（Schedule）**：基于Cron表达式的定时任务
- **事件触发（Event）**：响应飞书事件（消息、文档更新等）
- **条件触发（Condition）**：基于自定义条件的触发
- **手动触发（Manual）**：手动启动工作流
- **API触发（API）**：通过API接口触发

##### 1.2 工作流步骤（Step）
支持7种步骤类型：
- **API调用**：调用飞书或其他API
- **条件判断**：逻辑分支控制
- **数据处理**：数据过滤、排序、聚合
- **发送通知**：飞书消息、邮件通知
- **子工作流**：嵌套工作流调用
- **代码执行**：执行自定义Python代码
- **插件调用**：调用插件系统

##### 1.3 操作符支持（OperatorType）
支持13种比较操作符：
- `eq`（等于）、`ne`（不等于）
- `gt`（大于）、`lt`（小于）
- `ge`（大于等于）、`le`（小于等于）
- `in`（包含）、`not_in`（不包含）
- `is_null`（为空）、`not_null`（不为空）
- `is_true`（为真）、`not_true`（不为真）
- `in_list`（在列表中）

##### 1.4 工作流执行引擎
- 支持顺序执行和并行执行
- 失败重试机制（可配置重试次数）
- 失败继续执行模式
- 上下文数据传递
- 详细的执行日志

##### 1.5 事件处理系统
- 事件处理器注册
- 事件数据传递
- 异常处理和错误捕获

#### 使用示例

```python
from workflows.engine import WorkflowEngine, Trigger, Step, TriggerType, StepType

# 创建工作流引擎
engine = WorkflowEngine()

# 创建工作流
workflow_id = engine.create_workflow(
    "daily_sales_report",
    "每日销售报告",
    "每天自动生成销售报告"
)

# 添加定时触发器（每天9点）
trigger = Trigger(
    "daily_trigger_9am",
    TriggerType.SCHEDULE,
    {"schedule": "0 9 * * *"}  # Cron表达式
)
engine.add_trigger(workflow_id, trigger)

# 添加步骤
step1 = Step("get_sales", StepType.API_CALL, "获取销售数据", {
    "api": {
        "endpoint": "/api/bitable/records",
        "method": "GET",
        "params": {"app_token": "xxx", "table_id": "xxx"}
    }
})

step2 = Step("process_data", StepType.DATA_PROCESSING, "处理数据", {
    "operation": "filter",
    "params": {"field": "状态", "value": "已售出"}
})

# 执行工作流
result = engine.execute_workflow(workflow_id, context={"data": []})
print(result)
```

---

### 2. 📊 数据可视化（Data Visualization）

**模块位置**：`visualization/dashboard.py`
**代码行数**：约450行

#### 核心功能

##### 2.1 仪表盘生成器
- 自动布局生成
- 支持多种图表组合
- 动态数据适配
- 响应式设计

##### 2.2 图表类型支持（6种）
- **柱状图（Bar）**：数据对比分析
- **折线图（Line）**：趋势分析
- **饼图（Pie）**：占比分析
- **散点图（Scatter）**：相关性分析
- **热力图（Heatmap）**：二维数据分布
- **直方图（Histogram）**：数据分布分析

##### 2.3 双引擎支持
- **Plotly引擎**：交互式图表，支持Web展示
- **Matplotlib引擎**：静态图表，支持导出PNG

##### 2.4 导出功能
- PNG图片导出
- HTML仪表盘导出
- Excel报表生成

#### 使用示例

```python
from visualization.dashboard import DataVisualizer

# 创建可视化器
viz = DataVisualizer(style="plotly")

# 创建仪表盘
result = viz.create_dashboard(data, layout)
print(result)

# 创建图表
viz.create_chart(
    data=dataset,
    chart_type="bar",
    title="销售额统计",
    x="日期",
    y="金额"
)

# 创建热力图
viz.create_heatmap(
    data=dataframe,
    title="销售热力图",
    x="地区",
    y="产品"
)

# 导出图表
filename = viz.export_chart(fig, "sales_chart.png")
print(f"图表已导出: {filename}")
```

---

### 3. 🔌 插件系统（Plugin System）

**模块位置**：`plugins/plugin_system.py`
**代码行数**：约330行

#### 核心功能

##### 3.1 插件基类（Plugin）
抽象基类，定义插件标准接口：
- `execute(params, context)`：执行插件功能
- `get_config_schema()`：获取配置schema
- `get_info()`：获取插件信息
- `enable()`/`disable()`：启用/禁用插件
- `update_config(config)`：更新配置

##### 3.2 插件管理器（PluginManager）
管理插件的生命周期：
- 插件注册与加载
- 插件启用/禁用
- 插件查询和过滤
- 插件统计信息
- 插件导出

##### 3.3 钩子系统（Hooks）
支持插件钩子函数：
- 钩子函数注册
- 钩子执行时机控制
- 钩子参数传递

##### 3.4 配置验证
- JSON Schema验证
- 必需字段检查
- 数据类型验证

#### 使用示例

```python
from plugins.plugin_system import Plugin, PluginManager
from typing import Dict, Any

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__(
            plugin_id="my_plugin",
            name="我的插件",
            version="1.0.0",
            description="示例插件",
            author="三金的小虾米"
        )
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        # 执行插件逻辑
        result = {"success": True, "data": "执行成功"}
        return result
    
    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "api_key": {"type": "string"},
                "timeout": {"type": "integer"}
            },
            "required": ["api_key"]
        }

# 注册插件
manager = PluginManager()
plugin = MyPlugin()
manager.register_plugin(plugin)

# 启用插件
manager.enable_plugin("my_plugin")

# 查询插件
plugins = manager.list_plugins()
print(plugins)

# 获取统计信息
stats = manager.get_statistics()
print(stats)
```

---

### 4. 📦 示例插件

#### 4.1 库存预警插件

**模块位置**：`plugins/examples/inventory_alert_plugin.py`
**代码行数**：约230行

##### 功能描述
- 自动监控商品库存
- 当库存低于最小库存时触发预警
- 通过飞书消息发送通知
- 支持多个商品同时监控

##### 配置schema
```json
{
  "type": "object",
  "properties": {
    "min_stock_alert": {
      "type": "boolean",
      "description": "是否启用库存预警",
      "default": true
    },
    "alert_method": {
      "type": "string",
      "description": "预警方式",
      "enum": ["message", "email"],
      "default": "message"
    },
    "recipient": {
      "type": "string",
      "description": "接收人ID"
    },
    "app_id": {
      "type": "string",
      "description": "飞书应用ID"
    },
    "app_secret": {
      "type": "string",
      "description": "飞书应用密钥"
    },
    "table_id": {
      "type": "string",
      "description": "数据表ID"
    },
    "min_stock_column": {
      "type": "string",
      "description": "最小库存字段名"
    },
    "current_stock_column": {
      "type": "string",
      "description": "当前库存字段名"
    },
    "product_name_column": {
      "type": "string",
      "description": "商品名称字段名"
    }
  },
  "required": [
    "min_stock_alert",
    "min_stock_column",
    "current_stock_column",
    "product_name_column"
  ]
}
```

##### 使用示例
```python
from plugins.examples.inventory_alert_plugin import InventoryAlertPlugin

# 创建插件
plugin = InventoryAlertPlugin()

# 配置插件
plugin.update_config({
    "recipient": "ou_xxx",
    "app_id": "cli_xxx",
    "app_secret": "xxx",
    "table_id": "tbl_xxx",
    "min_stock_column": "最小库存",
    "current_stock_column": "当前库存",
    "product_name_column": "商品名称"
})

# 执行插件
result = plugin.execute(
    params={},
    context={
        "data": [
            {"商品名称": "产品A", "当前库存": 5, "最小库存": 10},
            {"商品名称": "产品B", "当前库存": 20, "最小库存": 10}
        ]
    }
)
print(result)
```

---

### 5. 📋 示例工作流

#### 5.1 每日销售报告工作流

**模块位置**：`workflows/examples/daily_sales_report_workflow.py`
**代码行数**：约80行

##### 工作流步骤
1. **获取销售数据**：从飞书多维表格读取销售数据
2. **过滤数据**：筛选"已售出"状态的订单
3. **计算销售额**：汇总销售总金额
4. **生成报告**：创建飞书文档，生成销售报告

##### 工作流定义
```json
{
  "id": "daily_sales_report",
  "name": "每日销售报告生成",
  "description": "每天定时生成销售报告",
  "version": "1.0.0",
  "triggers": [
    {
      "id": "daily_trigger",
      "type": "schedule",
      "schedule": "0 9 * *",
      "description": "每天9点触发"
    }
  ],
  "steps": [
    {
      "id": "step1",
      "name": "获取销售数据",
      "type": "api_call",
      "config": {
        "api_endpoint": "/api/bitable/records",
        "method": "GET",
        "params": {
          "app_token": "AXDyb30BNamJJ6sMYh2cda7Gnxg",
          "table_id": "tblcpk0OtPpxNwrs"
        }
      }
    },
    {
      "id": "step2",
      "name": "处理数据",
      "type": "data_processing",
      "operation": "filter",
      "params": {
        "field": "状态",
        "value": "已售出"
      }
    },
    {
      "id": "step3",
      "name": "计算销售额",
      "type": "data_processing",
      "operation": "aggregate",
      "params": {
        "field": "金额",
        "function": "sum"
      }
    },
    {
      "id": "step4",
      "name": "生成报告",
      "type": "doc",
      "config": {
        "api_endpoint": "/api/doc/documents",
        "method": "POST",
        "params": {
          "title": "每日销售报告-20260330",
          "content": "# 每日销售报告\n\n## 销售额总计：xxx\n"
        }
      }
    }
  ]
}
```

##### 使用示例
```python
from workflows.examples.daily_sales_report_workflow import main, export_workflow

# 导入工作流定义
workflow = main()

# 导出工作流为JSON
filename = export_workflow(workflow, "daily_sales_report.json")
print(f"工作流已导出: {filename}")
```

---

## 🔧 修复的问题

### 代码错误修复
1. **visualization/dashboard.py**
   - 修复重复的配置设置
   - 修复类型错误（List[Dict] vs DataFrame）
   - 修复`create_heatmap`函数中的括号不匹配
   - 修复`create_histogram`函数中的注释错误
   - 修复`save_report`函数中的ExcelWriter参数错误
   - 修复`export_chart`函数中的重复替换
   - 修复`export_dashboard`函数中的未定义属性引用
   - 修复`_auto_layout`函数中的字典键访问错误

2. **workflows/engine.py**
   - 修复lambda函数参数错误（`IS_NULL`操作符）
   - 修复`continue_on_failure`方法使用Python关键字的问题
   - 修复f-string语法错误（缺少闭合括号）

3. **plugins/plugin_system.py**
   - 修复`register_plugin`方法的docstring格式错误
   - 修复`list_plugins`和`get_plugins_by_type`方法中的逻辑错误
   - 修复`get_statistics`方法中的列表推导式错误
   - 修复变量名引用错误（`plugin.id` → `p.plugin_id`）

4. **plugins/examples/inventory_alert_plugin.py**
   - 修复`get_config_schema`中的类型定义重复错误
   - 修复`execute`方法中的变量引用错误
   - 修复`_send_notification`方法中的未定义变量引用
   - 修复返回语句逻辑错误

5. **feishu_core/base.py**
   - 修复`__init__.py`中的缩进错误

---

## 📊 代码统计

### 文件统计
| 类型 | 数量 | 代码行数 |
|------|------|----------|
| 核心模块 | 10 | ~5,490行 |
| 工作流引擎 | 1 | ~600行 |
| 数据可视化 | 1 | ~450行 |
| 插件系统 | 1 | ~330行 |
| 示例插件 | 1 | ~230行 |
| 示例工作流 | 1 | ~80行 |
| **总计** | **17** | **~5,490行** |

### 功能统计
- 工作流步骤类型：7种
- 触发器类型：5种
- 操作符类型：13种
- 图表类型：6种
- 渲染引擎：2种

---

## 🚀 升级指南

### 从v1.2.0升级到v2.0.0

```bash
# 拉取最新代码
git pull origin main

# 安装新增依赖
pip install plotly kaleido matplotlib seaborn pandas

# 验证安装
python -c "from workflows.engine import WorkflowEngine; print('工作流引擎安装成功')"
python -c "from visualization.dashboard import DataVisualizer; print('数据可视化安装成功')"
python -c "from plugins.plugin_system import PluginManager; print('插件系统安装成功')"
```

### 依赖更新
新增依赖：
- `plotly>=5.14.0`：交互式图表
- `kaleido>=0.2.1`：Plotly图片导出
- `matplotlib>=3.7.0`：静态图表
- `seaborn>=0.12.0`：数据可视化主题

---

## 📚 文档更新

### 新增文档
- 工作流引擎使用指南（准备中）
- 数据可视化教程（准备中）
- 插件开发指南（准备中）
- 示例插件文档（准备中）

### 更新文档
- README.md：添加v2.0.0功能介绍
- 开发路线图：标记v1.2.0和v2.0.0已完成

---

## 🤝 贡献者

- **三金的小虾米**（主要开发者）
  - 邮箱：1309244704@qq.com
  - GitHub：https://github.com/LX1309244704

---

## 🔗 相关链接

- GitHub仓库：https://github.com/LX1309244704/feishu-py-tools
- 问题反馈：https://github.com/LX1309244704/feishu-py-tools/issues
- 功能请求：https://github.com/LX1309244704/feishu-py-tools/issues

---

## 🎯 下一步计划

### v2.1.0 计划中
- [ ] Web UI界面
- [ ] 更多示例插件
- [ ] 更多示例工作流
- [ ] 性能优化
- [ ] 单元测试完善

### v3.0.0 长期计划
- [ ] 分布式工作流
- [ ] 实时数据监控
- [ ] 机器学习集成
- [ ] 移动端支持

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**🦞 飞书Python工具箱 v2.0.0 - 让飞书管理更智能、更高效！**
