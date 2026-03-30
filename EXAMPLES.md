# 飞书Python工具箱使用示例

## 快速开始

### 1. 安装

```bash
# 克隆项目
git clone https://github.com/LX1309244704/weiyuan.git
cd weiyuan

# 安装依赖
pip install -r requirements.txt

# 安装工具
pip install -e .
```

### 2. 配置

```bash
# 初始化配置
feishu-cli config init

# 编辑配置文件
nano ~/.weiyuan/config.yaml
```

配置文件示例：
```yaml
feishu:
  app_id: "cli_xxxxxxxxxxxxxxxx"
  app_secret: "xxxxxxxxxxxxxxxxxxxxxxxx"
  encrypt_key: ""
  verification_token: ""

ai:
  claude:
    api_key: ""
    model: "claude-3-5-sonnet-20241022"
  openai:
    api_key: ""
    model: "gpt-4o"

database:
  type: "sqlite"
  path: "~/.weiyuan/data.db"
```

### 3. 获取飞书应用凭据

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建应用
3. 获取 App ID 和 App Secret
4. 配置权限：
   - bitable:app（多维表格）
   - docx:document（文档）
   - contact:user.base（用户信息）

---

## 命令行使用

### 多维表格管理

```bash
# 列出所有多维表格
feishu-cli base list

# 创建新表格
feishu-cli base create --name "客户管理" --template crm

# 查看表格记录
feishu-cli base list --app-token AXDyb30BNamJJ6sMYh2cda7Gnxg --table-id tblL78Q0FtgmqcyQ

# 导入数据
feishu-cli base import --app-token xxx --table-id xxx --file data.csv

# 导出数据
feishu-cli base export --app-token xxx --table-id xxx --format csv --output output.csv
```

### 文档管理

```bash
# 创建文档
feishu-cli doc create --title "项目计划" --content "# 项目计划\n\n这里是内容"

# 读取文档
feishu-cli doc read --doc-id doc_xxxxxxx
```

### 工作流管理

```bash
# 列出所有工作流
feishu-cli workflow list-workflows

# 运行工作流
feishu-cli workflow run --config workflow.yaml
```

### AI集成

```bash
# 自然语言查询
feishu-cli ai query --prompt "查询本周完成的任务数量"

# 智能推荐
feishu-cli ai recommend --scenario "客户管理"
```

### 数据可视化

```bash
# 生成仪表盘
feishu-cli viz dashboard --app-token xxx --table-id xxx
```

---

## Python API 使用

### 1. 多维表格管理

```python
from feishu_core.bitable_manager import BitableManager

# 初始化
manager = BitableManager(
    app_id="cli_xxxxxxxxxxxxxxxx",
    app_secret="xxxxxxxxxxxxxxxxxxxxxxxx"
)

# 列出数据表
tables = manager.list_tables("AXDyb30BNamJJ6sMYh2cda7Gnxg")
for table in tables:
    print(f"表格名称: {table['name']}")
    print(f"表格ID: {table['table_id']}")

# 查看记录
records = manager.list_records(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblL78Q0FtgmqcyQ"
)
for record in records.get("items", []):
    print(record["fields"])

# 创建记录
record_id = manager.create_record(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblL78Q0FtgmqcyQ",
    fields={
        "员工姓名": "张三",
        "工号": "EMP004",
        "职位": "销售经理",
        "手机号": "13800138004",
        "邮箱": "zhangsan4@example.com"
    }
)
print(f"创建成功，记录ID: {record_id}")

# 批量创建记录
new_records = [
    {
        "员工姓名": "李四",
        "工号": "EMP005",
        "职位": "销售专员"
    },
    {
        "员工姓名": "王五",
        "工号": "EMP006",
        "职位": "销售主管"
    }
]
record_ids = manager.batch_create_records(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblL78Q0FtgmqcyQ",
    records=new_records
)
print(f"批量创建成功，创建了 {len(record_ids)} 条记录")

# 更新记录
success = manager.update_record(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblL78Q0FtgmqcyQ",
    record_id="recvffyEPqScvj",
    fields={
        "职位": "高级销售经理"
    }
)
print(f"更新成功: {success}")

# 删除记录
success = manager.delete_record(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblL78Q0FtgmqcyQ",
    record_id="recvffyEPqScvj"
)
print(f"删除成功: {success}")

# 搜索记录
filtered = manager.search_records(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblL78Q0FtgmqcyQ",
    filter_dict={"职位": "销售经理"}
)
for record in filtered:
    print(record)

# 导出数据到CSV
csv_file = manager.export_to_csv(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblL78Q0FtgmqcyQ",
    output_file="users.csv"
)
print(f"导出成功: {csv_file}")

# 从CSV导入数据
count = manager.import_from_csv(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblL78Q0FtgmqcyQ",
    csv_file="users.csv"
)
print(f"导入了 {count} 条记录")
```

### 2. 文档管理

```python
from feishu_core.doc_manager import DocManager

# 初始化
doc_manager = DocManager(
    app_id="cli_xxxxxxxxxxxxxxxx",
    app_secret="xxxxxxxxxxxxxxxxxxxxxxxx"
)

# 创建文档
doc_id = doc_manager.create_document(
    title="项目计划",
    content="# 项目计划\n\n## 目标\n完成XXX项目开发\n\n## 任务\n1. 需求分析\n2. 系统设计\n3. 开发实现\n4. 测试部署"
)
print(f"创建成功，文档ID: {doc_id}")

# 获取文档内容
doc_content = doc_manager.get_document(doc_id)
print(doc_content)

# 列出文档
documents = doc_manager.list_documents()
for doc in documents:
    print(f"文档名称: {doc['name']}")
    print(f"文档ID: {doc['token']}")

# 添加评论
comment_id = doc_manager.add_comment(
    document_id=doc_id,
    content="这个计划看起来不错，我建议增加一个风险分析的章节"
)
print(f"评论成功，评论ID: {comment_id}")

# 获取评论
comments = doc_manager.get_comments(doc_id)
for comment in comments:
    print(f"评论: {comment['body']['content']}")

# 删除文档
success = doc_manager.delete_document(doc_id)
print(f"删除成功: {success}")
```

### 3. 配置管理

```python
from feishu_cli.config import ConfigManager

# 初始化配置
config = ConfigManager()
config.init_config()

# 加载配置
config.load_config()

# 获取配置
app_id = config.get("feishu.app_id")
print(f"App ID: {app_id}")

# 设置配置
config.set("feishu.app_id", "cli_xxxxxxxxxxxxxxxx")
config.set("ai.claude.api_key", "sk-xxxxxxxxxxxx")

# 验证配置
if config.validate_config():
    print("配置有效")
else:
    print("配置无效")

# 获取授权URL
auth_url = config.get_auth_url()
print(f"请访问此链接授权: {auth_url}")
```

---

## 实际应用场景

### 场景1：电商进销存管理

```python
from feishu_core.bitable_manager import BitableManager

manager = BitableManager()

# 添加新商品
manager.create_record(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblcpk0OtPpxNwrs",
    fields={
        "商品名称": "iPhone 16 Pro",
        "商品编号": "SKU006",
        "单价": 9999,
        "当前库存": 100,
        "最小库存": 20,
        "供应商": "Apple官方直营"
    }
)

# 添加新客户
manager.create_record(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblfv9mrEIt5RZIS",
    fields={
        "客户姓名": "张总",
        "客户编号": "CUST006",
        "公司名称": "ABC科技公司",
        "联系电话": "13900139006",
        "邮箱": "zhang@abctech.com"
    }
)

# 生成销售报告
sales_data = manager.list_records(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblcpk0OtPpxNwrs"
)

total_value = 0
for item in sales_data.get("items", []):
    fields = item["fields"]
    if "单价" in fields and "当前库存" in fields:
        total_value += fields["单价"] * fields["当前库存"]

print(f"总库存价值: ¥{total_value:,}")
```

### 场景2：项目进度跟踪

```python
from feishu_core.bitable_manager import BitableManager
from feishu_core.doc_manager import DocManager

bitable = BitableManager()
doc = DocManager()

# 创建项目文档
doc_id = doc.create_document(
    title="项目进度报告",
    content=f"""
# 项目进度报告

## 本周完成情况
1. 完成了用户管理系统的开发
2. 完成了进销存管理系统的开发
3. 完成了客户联系表的创建

## 下周计划
1. 完善系统功能
2. 添加自动化工作流
3. 进行测试和部署

## 风险与问题
1. 需要更多的API调用额度
2. 需要优化数据导入导出功能
"""
)

# 更新项目进度记录
bitable.create_record(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblL78Q0FtgmqcyQ",
    fields={
        "员工姓名": "张三",
        "任务": "系统开发",
        "进度": "80%",
        "状态": "进行中"
    }
)
```

### 场景3：数据分析

```python
from feishu_core.bitable_manager import BitableManager
import pandas as pd

manager = BitableManager()

# 导出数据到CSV
csv_file = manager.export_to_csv(
    app_token="AXDyb30BNamJJ6sMYh2cda7Gnxg",
    table_id="tblcpk0OtPpxNwrs",
    output_file="products.csv"
)

# 使用Pandas分析数据
df = pd.read_csv(csv_file)

# 计算总库存价值
df["总价值"] = df["单价"] * df["当前库存"]
total_value = df["总价值"].sum()

# 统计库存不足的商品
low_stock = df[df["当前库存"] < df["最小库存"]]

print(f"总库存价值: ¥{total_value:,}")
print(f"\n库存不足的商品 ({len(low_stock)} 个):")
for idx, row in low_stock.iterrows():
    print(f"- {row['商品名称']}: 当前库存 {row['当前库存']}, 最小库存 {row['最小库存']}")
```

---

## 故障排查

### 1. 配置问题

```bash
# 检查配置文件
cat ~/.weiyuan/config.yaml

# 验证配置
python -c "from feishu_cli.config import ConfigManager; c = ConfigManager(); print('配置有效' if c.validate_config() else '配置无效')"
```

### 2. 权限问题

确保在飞书开放平台配置了以下权限：
- bitable:app
- docx:document
- contact:user.base

### 3. 网络问题

```bash
# 测试飞书API连接
curl -X GET https://open.feishu.cn/open-apis/server/info
```

---

## 更多资源

- [官方文档](https://github.com/LX1309244704/weiyuan)
- [飞书开放平台](https://open.feishu.cn/)
- [ClawHub技能市场](https://clawhub.ai/)

---

**版本**: v1.0.0  
**作者**: 三金的小虾米  
**邮箱**: 1309244704@qq.com
