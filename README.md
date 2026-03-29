# FeiShu-Py-Tools - 飞书Python工具箱

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Feishu](https://img.shields.io/badge/Feishu-Lark-orange.svg)](https://www.feishu.cn)

> 基于飞书官方CLI的Python增强版飞书管理工具，专注多维表格自动化和AI集成

## 🌟 项目简介

**FeiShu-Py-Tools**是一个功能强大的飞书Python工具箱，在飞书官方CLI基础上，增强了多维表格自动化、AI集成、工作流自动化和数据可视化能力。

### ✨ 核心特性

- 🚀 **更易使用**：Python语言，比Go CLI更易上手
- 🤖 **AI集成**：原生支持Claude、GPT、本地LLM
- 📊 **多维表格增强**：批量导入导出、智能数据清洗、自动化工作流
- 🔄 **工作流引擎**：可视化流程设计、条件触发、任务编排
- 📈 **数据可视化**：一键生成仪表盘、实时数据同步、交互式图表
- 💡 **智能助手**：自然语言查询、智能推荐、数据洞察

---

## 📊 功能模块

### 1. 多维表格管理（BitableManager）⭐

**核心功能**：
- ✅ 创建/读取/更新/删除记录（CRUD）
- ✅ 批量操作支持
- ✅ 数据导入导出（CSV格式）
- ✅ 记录搜索和筛选
- ✅ 分页查询支持

**应用场景**：
- CRM客户管理
- 进销存管理
- 数据收集表单
- 资产管理系统
- 销售漏斗管理

### 2. 文档管理（DocManager）

**核心功能**：
- ✅ 创建/读取/更新/删除文档
- ✅ 添加评论
- ✅ 获取评论列表
- ✅ 列出文档
- ✅ Markdown格式支持

**应用场景**：
- 项目文档管理
- 知识库管理
- 协作文档
- 会议纪要
- 技术文档

### 3. 日历管理（CalendarManager）🆕

**核心功能**：
- ✅ 获取主日历和日历列表
- ✅ 创建/读取/更新/删除日程
- ✅ 查询用户忙闲状态
- ✅ 日程搜索
- ✅ 参会人管理

**应用场景**：
- 会议安排
- 日程管理
- 团队协作
- 项目计划
- 提醒通知

### 4. 任务管理（TaskManager）🆕

**核心功能**：
- ✅ 创建/读取/更新/删除任务
- ✅ 任务清单管理
- ✅ 子任务支持
- ✅ 任务评论
- ✅ 任务搜索

**应用场景**：
- 项目任务跟踪
- 待办事项管理
- 任务分配
- 进度跟踪
- 团队协作

### 5. 消息管理（MessageManager）🆕

**核心功能**：
- ✅ 发送文本/图片/文件消息
- ✅ 发送卡片消息
- ✅ 发送富文本消息
- ✅ 回复和撤回消息
- ✅ 获取聊天记录
- ✅ 通知消息

**应用场景**：
- 自动通知
- 系统提醒
- 消息推送
- 客户服务
- 团队沟通

### 6. 配置管理（ConfigManager）

**核心功能**：
- ✅ 配置文件初始化
- ✅ 配置读写操作
- ✅ 配置验证
- ✅ 嵌套配置支持
- ✅ 飞书授权URL生成

### 7. AI集成模块（AI Integration）🆕 v1.2.0

**核心功能**：
- ✅ 多模型支持（Claude 3.5、GPT-4、DeepSeek）
- ✅ 自然语言查询处理器
- ✅ 智能推荐引擎
- ✅ 数据清洗器
- ✅ 流式聊天支持
- ✅ 函数调用接口
- ✅ 情感分析
- ✅ 文本摘要
- ✅ 实体提取
- ✅ 代码审查

**支持模型**：
- **Claude 3.5 Sonnet**：复杂推理、长文本处理
- **GPT-4 Omni**：快速生成、多模态能力
- **DeepSeek R1**：低成本国产模型

**应用场景**：
- AI数据分析
- 自然语言查询
- 智能推荐系统
- 自动化文案生成
- 代码辅助开发
- 数据质量清洗

---

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/LX1309244704/feishu-py-tools.git
cd feishu-py-tools

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
feishu-py-tools/
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

| 特性 | 飞书官方CLI | FeiShu-Py-Tools |
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

### ✅ v1.0.0 已完成
- [x] 项目架构设计
- [x] 核心功能模块框架
- [x] 飞书CLI集成层
- [x] 多维表格管理（BitableManager）
- [x] 文档管理（DocManager）
- [x] 配置管理（ConfigManager）

### ✅ v1.1.0 已完成 🆕
- [x] 日历管理（CalendarManager）
- [x] 任务管理（TaskManager）
- [x] 消息管理（MessageManager）
- [x] 完善文档管理功能

### 🚧 v1.2.0 计划中
- [ ] AI集成（Claude、GPT、DeepSeek）
- [ ] 自然语言查询
- [ ] 智能推荐系统
- [ ] 数据清洗功能

### 📅 v2.0.0 计划中
- [ ] Web UI界面
- [ ] 完整的工作流引擎
- [ ] 高级数据可视化
- [ ] 插件系统
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
