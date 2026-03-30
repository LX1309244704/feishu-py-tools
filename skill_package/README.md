# Weiyuan - 飞书Python工具箱

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Feishu](https://img.shields.io/badge/Feishu-Lark-orange.svg)](https://www.feishu.cn)

> 基于飞书官方CLI的Python增强版飞书管理工具，专注多维表格自动化和AI集成

## 🌟 项目简介

**Weiyuan**是一个功能强大的飞书Python工具箱，在飞书官方CLI基础上，增强了多维表格自动化、AI集成、工作流自动化和数据可视化能力。

### ✨ 核心特性

- 🚀 **更易使用**：Python语言，比Go CLI更易上手
- 🤖 **AI集成**：原生支持Claude、GPT、本地LLM
- 📊 **多维表格增强**：批量导入导出、智能数据清洗、自动化工作流
- 🔄 **工作流引擎**：可视化流程设计、条件触发、任务编排
- 📈 **数据可视化**：一键生成仪表盘、实时数据同步、交互式图表
- 💡 **智能助手**：自然语言查询、智能推荐、数据洞察

---

## 📊 功能模块

### 1. 多维表格增强模块（lark-base-enhanced）

**核心功能**：
- ✅ 自动化字段生成（根据业务场景）
- ✅ 智能数据填充（AI辅助录入）
- ✅ 批量导入导出（Excel、CSV、JSON）
- ✅ 数据清洗（去重、标准化、校验）
- ✅ 公式字段自动创建
- ✅ 高级视图管理
- ✅ 仪表盘生成
- ✅ 工作流触发器

**应用场景**：
- CRM客户管理
- 项目进度跟踪
- 数据收集表单
- 资产管理系统
- 销售漏斗管理

### 2. 文档协作增强模块（lark-doc-enhanced）

**核心功能**：
- ✅ 文档模板库
- ✅ AI辅助写作
- ✅ 智能纠错
- ✅ 格式优化
- ✅ 协作评论处理
- ✅ 版本管理
- ✅ 全文搜索

### 3. 工作流自动化模块（workflow-engine）

**核心功能**：
- ✅ 可视化流程设计
- ✅ 条件判断
- ✅ 任务编排
- ✅ 事件触发
- ✅ 错误处理
- ✅ 日志审计
- ✅ 性能监控

### 4. AI集成模块（ai-integration）

**核心功能**：
- ✅ 多模型支持（Claude、GPT、本地LLM）
- ✅ 智能推荐
- ✅ 自动分类
- ✅ 数据洞察
- ✅ 自然语言查询
- ✅ 智能提醒

### 5. 数据可视化模块（data-visualization）

**核心功能**：
- ✅ 仪表盘生成
- ✅ 图表组件（柱状图、饼图、折线图、甘特图）
- ✅ 实时更新
- ✅ 交互式图表
- ✅ 报表导出（PDF、Excel、PNG）

---

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/LX1309244704/weiyuan.git
cd weiyuan

# 安装依赖
pip install -r requirements.txt

# 安装工具
pip install -e .
```

### 配置

```bash
# 初始化配置
feishu-cli config init

# 扫码授权
# 按照提示完成飞书应用授权
```

### 基本使用

#### 命令行使用

```bash
# 查看多维表格列表
feishu-cli base list

# 创建多维表格
feishu-cli base create --name "客户管理表" --template "crm"

# 导入数据
feishu-cli base import --app-token xxx --table-id xxx --file data.csv

# 导出数据
feishu-cli base export --app-token xxx --table-id xxx --format csv

# AI辅助录入
feishu-cli base ai-fill --app-token xxx --table-id xxx --prompt "添加10个客户信息"
```

#### Python API使用

```python
from feishu_core.base import BitableManager

# 初始化
manager = BitableManager(
    app_id="cli_xxx",
    app_secret="xxx"
)

# 获取表格列表
tables = manager.list_tables()
print(tables)

# 创建记录
manager.create_record(
    app_token="xxx",
    table_id="xxx",
    fields={
        "客户名称": "ABC公司",
        "联系方式": "13800138000",
        "需求描述": "需要开发智能客服机器人",
        "项目进度": "进行中"
    }
)

# 批量导入
manager.import_from_csv(
    app_token="xxx",
    table_id="xxx",
    csv_file="data.csv"
)

# 导出数据
data = manager.export_to_csv(
    app_token="xxx",
    table_id="xxx"
)
print(data)
```

---

## 📚 项目结构

```
weiyuan/
├── README.md                    # 项目说明
├── requirements.txt             # 依赖文件
├── setup.py                     # 安装脚本
├── feishu_cli/                  # CLI入口
│   ├── __init__.py
│   ├── main.py                  # 主入口
│   ├── commands/                # CLI命令
│   └── config.py                # 配置管理
├── feishu_core/                 # 核心功能
│   ├── __init__.py
│   ├── base.py                  # 多维表格
│   ├── doc.py                   # 文档
│   ├── task.py                  # 任务
│   ├── calendar.py              # 日历
│   ├── message.py               # 消息
│   ├── drive.py                 # 云空间
│   └── cli_wrapper.py          # CLI包装器
├── workflows/                    # 工作流
│   ├── __init__.py
│   ├── engine.py                # 工作流引擎
│   ├── triggers.py              # 触发器
│   └── tasks.py                 # 任务
├── ai_integration/               # AI集成
│   ├── __init__.py
│   ├── models.py                # AI模型
│   ├── assistant.py              # AI助手
│   └── processors.py            # AI处理器
├── visualization/                # 数据可视化
│   ├── __init__.py
│   ├── dashboard.py             # 仪表盘
│   ├── charts.py                # 图表
│   └── reports.py               # 报表
├── templates/                    # 模板
│   ├── base/                    # 多维表格模板
│   ├── doc/                     # 文档模板
│   └── workflow/                # 工作流模板
└── tests/                       # 测试
    ├── test_base.py
    ├── test_doc.py
    └── test_workflow.py
```

---

## 💡 使用场景

### 场景1：CRM客户管理

```python
from feishu_core.base import BitableManager

# 初始化
manager = BitableManager()

# 使用CRM模板创建表格
table_id = manager.create_table_from_template("crm")

# AI辅助录入客户信息
manager.ai_fill(
    app_token="xxx",
    table_id=table_id,
    prompt="添加10个客户信息，包括公司名称、联系方式、需求描述",
    model="claude"
)

# 生成仪表盘
from visualization.dashboard import DashboardGenerator
gen = DashboardGenerator()
gen.create_dashboard(
    app_token="xxx",
    table_id=table_id,
    charts=["客户分布", "项目进度", "销售漏斗"]
)
```

### 场景2：项目进度跟踪

```python
from workflows.engine import WorkflowEngine
from feishu_core.base import BitableManager

# 定义工作流
engine = WorkflowEngine()

# 创建项目表格
manager = BitableManager()
table_id = manager.create_table_from_template("project")

# 配置工作流
engine.add_trigger(
    condition="任务状态变更",
    action="更新仪表盘"
)

engine.add_trigger(
    condition="任务到期",
    action="发送提醒"
)

# 执行工作流
engine.run()
```

### 场景3：AI智能助手

```python
from ai_integration.assistant import FeishuAssistant

# 初始化助手
assistant = FeishuAssistant(
    model="claude",
    api_key="xxx"
)

# 自然语言查询
result = assistant.query(
    "查询本周完成的任务数量",
    app_token="xxx",
    table_id="xxx"
)

print(result)

# 智能推荐
recommendations = assistant.recommend(
    "根据当前项目进度，推荐下一步行动",
    app_token="xxx",
    table_id="xxx"
)
print(recommendations)
```

---

## 🎯 核心优势

### 相比飞书官方CLI的优势

| 特性 | 飞书官方CLI | Weiyuan |
|------|-------------|-----------------|
| 语言 | Go | Python |
| 学习曲线 | 中 | 低 |
| AI集成 | 基础 | 强 |
| 多维表格增强 | 基础 | 强 |
| 工作流引擎 | 无 | 有 |
| 数据可视化 | 无 | 有 |
| Web UI | 无 | 有（计划） |
| 模板库 | 无 | 有 |
| 自然语言查询 | 无 | 有 |

---

## 📝 开发路线图

### ✅ 已完成
- [x] 项目架构设计
- [x] 核心功能模块框架
- [x] 飞书CLI集成层

### 🚧 进行中
- [ ] 多维表格增强功能
- [ ] AI集成模块
- [ ] 工作流引擎
- [ ] 数据可视化

### 📅 计划中
- [ ] Web UI界面
- [ ] 插件系统
- [ ] API服务接口
- [ ] 性能优化

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👥 作者

- **作者**：三金的小虾米
- **邮箱**：1309244704@qq.com
- **GitHub**：https://github.com/LX1309244704

---

## 🙏 致谢

- 感谢飞书官方开源的 [lark-cli](https://github.com/larksuite/cli)
- 感谢所有贡献者

---

**🦞 飞书Python工具箱 - 让飞书管理更智能、更高效！**
