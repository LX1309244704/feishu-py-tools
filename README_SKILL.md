# 🦞 胴体搭建系统 - Skill使用指南

## 📖 快速开始

### 1. 安装Skill包

```bash
# 克隆项目
git clone https://github.com/LX1309244704/weiyuan.git
cd weiyuan

# 安装依赖
pip install -r requirements.txt

# 安装工具
pip install -e .
```

### 2. 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置文件
nano .env
```

**环境变量说明**：

```env
# 飞书应用配置
FEISHU_APP_ID=cli_xxxxxx
FEISHU_APP_SECRET=xxxxxx
FEISHU_VERIFICATION_TOKEN=xxxxxx
FEISHU_ENCRYPT_KEY=xxxxxx

# AI模型配置
OPENAI_API_KEY=sk-xxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxx
DEEPSEEK_API_KEY=sk-xxxxxx

# 数据库配置（可选）
DATABASE_URL=postgresql://user:password@localhost/feishu_tools
REDIS_URL=redis://localhost:6379/0

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=/var/log/feishu_tools.log
```

### 3. 授权配置

```bash
# 初始化配置
feishu-cli config init

# 扫码授权
feishu-cli config auth
```

### 4. 验证安装

```bash
# 查看版本
feishu-cli --version

# 测试连接
feishu-cli base list
```

---

## 🎯 核心功能使用

### 功能1：系统快速搭建

#### 使用模板创建表格

```bash
# 创建公司信息管理表格
feishu-cli base create --name "公司信息管理" --template company

# 创建组织架构设计表格
feishu-cli base create --name "组织架构设计" --template organization

# 创建产品架构设计表格
feishu-cli base create --name "产品架构设计" --template product
```

#### Python API方式

```python
from feishu_core.base import BitableManager

manager = BitableManager()

# 使用模板创建表格
table_id = manager.create_table_from_template(
    template="company",
    name="公司信息管理"
)

print(f"表格创建成功，Table ID: {table_id}")
```

---

### 功能2：AI智能客户服务

#### AI辅助录入客户信息

```bash
# 命令行方式
feishu-cli base ai-fill \
  --app-token xxx \
  --table-id xxx \
  --prompt "添加10个AI行业的客户信息，包括公司名称、成立时间、行业、规模、联系人"
```

#### Python API方式

```python
from ai_integration.processor import AIDataProcessor

processor = AIDataProcessor(model="claude")

count = processor.process_prompt(
    app_token="xxx",
    table_id="xxx",
    prompt="添加10个AI行业的客户信息"
)

print(f"成功录入 {count} 条客户信息")
```

---

### 功能3：项目全生命周期管理

#### 创建项目表格

```bash
# 使用项目模板创建
feishu-cli base create --name "项目管理" --template project
```

#### 查看项目进度

```python
from feishu_core.base import BitableManager

manager = BitableManager()

# 获取项目列表
projects = manager.list_records(
    app_token="xxx",
    table_id="xxx"
)

for project in projects:
    print(f"项目：{project['项目名称']}，进度：{project['进度']}")
```

---

### 功能4：数据分析报表

#### 生成仪表盘

```bash
feishu-cli viz dashboard \
  --app-token xxx \
  --table-id xxx \
  --charts "客户分布,销售漏斗,项目进度"
```

#### Python API方式

```python
from visualization.dashboard import DashboardGenerator

generator = DashboardGenerator()

output = generator.create_dashboard(
    app_token="xxx",
    table_id="xxx",
    charts=["客户分布", "销售漏斗", "项目进度"]
)

print(f"仪表盘生成成功：{output}")
```

---

### 功能5：自动化工作流

#### 创建工作流配置

创建文件 `workflow.yaml`：

```yaml
name: 客户跟进自动化
description: 自动跟进客户，生成提醒
trigger:
  type: data_change
  table_id: xxx
  field: 状态
  value: 新建

steps:
  - id: step1
    name: 创建跟进任务
    api: task.create
    params:
      title: "跟进客户：${客户名称}"
      due: "+3d"
      assignee: ${USER_OPEN_ID}

  - id: step2
    name: 发送通知
    api: message.send
    params:
      chat_id: ${CHAT_ID}
      content: "有新客户需要跟进：${客户名称}"
```

#### 运行工作流

```bash
feishu-cli workflow run --config workflow.yaml
```

---

## 📚 8个模板使用说明

### 模板1：公司信息管理

**字段列表**：
- 公司名称（文本）
- 成立时间（日期）
- 创始人（文本）
- 行业（单选）
- 规模（单选：10-50人, 50-100人, 100-500人, 500+人）
- 融资（单选：天使轮, A轮, B轮, C轮, 已上市）
- 产品（多选）
- 官网（超链接）
- 联系人（文本）
- 备注（文本）

**使用示例**：

```python
from feishu_core.base import BitableManager

manager = BitableManager()

# 创建记录
manager.create_record(
    app_token="xxx",
    table_id="xxx",
    fields={
        "公司名称": "ABC科技公司",
        "成立时间": "2020-01-01",
        "创始人": "张三",
        "行业": "人工智能",
        "规模": "100-500人",
        "融资": "B轮",
        "产品": ["智能客服", "数据分析"],
        "官网": "https://www.abctech.com",
        "联系人": "张三",
        "备注": "专注于企业AI自动化"
    }
)
```

---

### 模板2：组织架构设计

**字段列表**：
- 部门名称（文本）
- 负责人（人员）
- 人数（数字）
- 预算（货币）
- 职能（文本）
- 目标（文本）
- KPI（文本）
- 备注（文本）

**使用示例**：

```python
manager.create_record(
    app_token="xxx",
    table_id="xxx",
    fields={
        "部门名称": "技术部",
        "负责人": "ou_xxx",
        "人数": 50,
        "预算": 5000000,
        "职能": "负责产品研发和技术架构",
        "目标": "Q4上线2个新产品",
        "KPI": "产品上线数、代码质量",
        "备注": "重点招聘AI工程师"
    }
)
```

---

### 模板3：产品架构设计

**字段列表**：
- 产品名称（文本）
- 版本（文本）
- 功能（多选）
- 用户画像（文本）
- 技术架构（文本）
- 依赖（多选）
- 路线图（文本）
- 备注（文本）

**使用示例**：

```python
manager.create_record(
    app_token="xxx",
    table_id="xxx",
    fields={
        "产品名称": "智能客服机器人",
        "版本": "v2.0",
        "功能": ["对话管理", "知识库", "工单系统"],
        "用户画像": "中小企业客服团队",
        "技术架构": "Python + Claude + Redis",
        "依赖": ["飞书API", "Claude API"],
        "路线图": "Q3：多模态支持，Q4：私有化部署",
        "备注": "重点优化响应速度"
    }
)
```

---

## 🤖 AI集成使用

### 1. 客户信息录入

```python
from ai_integration.processor import AIDataProcessor

processor = AIDataProcessor(model="claude")

prompt = """
录入以下客户信息：
公司：ABC科技公司
成立时间：2020年
规模：100-500人
行业：人工智能
创始人：张三
业务：企业AI自动化平台
联系方式：13800138000
邮件：contact@abctech.com
网址：www.abctech.com
"""

result = processor.process(prompt, app_token="xxx", table_id="xxx")
print(result)
```

**输出示例**：

```json
{
  "公司名称": "ABC科技公司",
  "联系人": "张三",
  "邮箱": "contact@abctech.com",
  "行业": "人工智能",
  "建议": "这类公司应该优先考虑购买『智能客服机器人』，成本仅为传统方案的1/3"
}
```

---

### 2. 销售数据分析

```python
from ai_integration.analyzer import DataAnalyzer

analyzer = DataAnalyzer(model="gpt-4")

prompt = """
分析以下销售数据：
2025年Q1业绩：1000万，增长30%
2025年Q2业绩：1500万，增长20%
2025年Q3业绩：1200万，-10%
趋势：2026Q1业绩：1800万，预期增长25%

请给出分析和建议
"""

insights = analyzer.analyze(prompt)
print(insights)
```

**输出示例**：

```json
{
  "分析": "Q3业绩下滑10%，需要重点关注。2026Q1预期增长25%，市场前景良好。",
  "建议": [
    "重点关注Q1的智能客服机器人产品线",
    "Q1市场份额可提升至15%",
    "自动化工具可降本30%"
  ]
}
```

---

### 3. 自然语言查询

```bash
# 命令行方式
feishu-cli ai query \
  --prompt "查询本周新增了多少客户" \
  --app-token xxx \
  --table-id xxx
```

```python
from ai_integration.assistant import FeishuAssistant

assistant = FeishuAssistant(model="claude")

result = assistant.query(
    prompt="查询本周新增了多少客户",
    app_token="xxx",
    table_id="xxx"
)

print(result)
```

---

## 🔄 工作流配置详解

### 场景：客户跟进自动化

#### 完整配置文件 `customer_followup.yaml`：

```yaml
name: 客户跟进自动化
description: 客户状态变更时自动创建跟进任务

# 触发器
trigger:
  type: data_change
  table_id: tblWpzyKj1W3juJS
  field: 状态
  value: 新建
  condition:
    - field: 优先级
      operator: is
      value: 高

# 步骤
steps:
  - id: step1
    name: 创建跟进任务
    api: task.create
    params:
      title: "跟进客户：${公司名称}"
      summary: "客户 ${公司名称} 需要跟进，优先级：${优先级}"
      due: "+3d"
      assignee: ${USER_OPEN_ID}

  - id: step2
    name: 发送通知
    api: message.send
    params:
      chat_id: ${CHAT_ID}
      content: |
        📢 新客户跟进提醒
        客户：${公司名称}
        联系人：${联系人}
        优先级：${优先级}
        请及时跟进

  - id: step3
    name: 更新客户状态
    api: base.record-update
    params:
      app_token: ${APP_TOKEN}
      table_id: ${TABLE_ID}
      record_id: ${RECORD_ID}
      fields:
        状态: 已分配
        分配时间: ${NOW}
```

#### 运行工作流

```bash
feishu-cli workflow run --config customer_followup.yaml
```

---

## 📊 数据可视化

### 创建销售漏斗图表

```python
from visualization.charts import ChartGenerator

generator = ChartGenerator()

# 创建销售漏斗
funnel = generator.create_funnel(
    data=[
        {"stage": "线索", "value": 100},
        {"stage": "意向", "value": 60},
        {"stage": "商机", "value": 30},
        {"stage": "成交", "value": 15}
    ],
    title="销售漏斗",
    output="sales_funnel.png"
)

print(f"图表已保存：{funnel}")
```

### 创建客户分布饼图

```python
# 创建客户分布饼图
pie = generator.create_pie(
    data=[
        {"industry": "人工智能", "value": 30},
        {"industry": "互联网", "value": 25},
        {"industry": "金融", "value": 20},
        {"industry": "其他", "value": 25}
    ],
    title="客户行业分布",
    output="customer_distribution.png"
)

print(f"图表已保存：{pie}")
```

---

## 🔧 高级功能

### 1. 批量导入数据

```python
from feishu_core.base import BitableManager

manager = BitableManager()

# 从CSV导入
count = manager.import_from_csv(
    app_token="xxx",
    table_id="xxx",
    csv_file="customers.csv"
)

print(f"成功导入 {count} 条记录")
```

### 2. 批量导出数据

```python
# 导出为CSV
data = manager.export_data(
    app_token="xxx",
    table_id="xxx",
    format="csv"
)

with open("export.csv", "w") as f:
    f.write(data)

print("数据已导出到 export.csv")
```

### 3. 智能数据清洗

```python
from ai_integration.cleaner import DataCleaner

cleaner = DataCleaner()

# 清洗数据
cleaned_data = cleaner.clean(
    data=raw_data,
    rules={
        "去重": "company_name",
        "标准化": "industry",
        "验证": "email"
    }
)

print(f"清洗后数据：{len(cleaned_data)} 条")
```

---

## 📝 常见问题

### Q1：如何获取飞书应用凭证？

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 创建应用
3. 获取 App ID 和 App Secret
4. 配置权限

### Q2：如何配置AI模型？

```bash
# 配置OpenAI
export OPENAI_API_KEY=sk-xxxxxx

# 配置Claude
export ANTHROPIC_API_KEY=sk-ant-xxxxxx

# 配置DeepSeek
export DEEPSEEK_API_KEY=sk-xxxxxx
```

### Q3：工作流如何调试？

```bash
# 启用调试模式
export DEBUG=true

# 运行工作流
feishu-cli workflow run --config workflow.yaml --verbose
```

---

## 🎯 最佳实践

### 1. 使用模板快速开始

```bash
# 列出所有模板
feishu-cli template list

# 使用模板创建
feishu-cli base create --name "客户管理" --template crm
```

### 2. AI辅助提高效率

```python
# 批量AI录入
for i in range(10):
    processor.process_prompt(
        app_token="xxx",
        table_id="xxx",
        prompt=f"添加第{i+1}个客户信息"
    )
```

### 3. 定期生成报表

```bash
# 创建定时任务
crontab -e

# 每周一早上9点生成周报
0 9 * * 1 feishu-cli viz dashboard --app-token xxx --table-id xxx
```

---

## 📞 技术支持

- **GitHub Issues**：https://github.com/LX1309244704/weiyuan/issues
- **邮箱**：1309244704@qq.com
- **虾评社区**：https://xiaping.coze.site
- **Instreet社区**：https://instreet.coze.site

---

**版本**：v1.0.0  
**更新日期**：2026-03-29  
**作者**：三金的小虾米

🦞 **想搭建系统的企业，就用飞书Python工具箱！**
