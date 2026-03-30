# 📊 完整实战演示：销售数据自动发布到抖音和微信

## 🎯 场景概述

**业务场景**：电商公司每天需要把飞书多维表格中的销售数据，自动发布到抖音和小红书做宣传，同时发送到企业微信群通知团队。

**自动化流程**：
```
飞书多维表格 
    ↓ (官方CLI获取数据)
销售数据 
    ↓ (AI生成文案)
抖音文案 + 小红书文案 
    ↓ (自动发布)
抖音 + 小红书 
    ↓ (发送通知)
企业微信群
```

---

## 📋 前置准备

### 1. 安装飞书官方 CLI

```bash
# 安装官方CLI
npm install -g @larksuite/cli

# 安装CLI Skill
npx skills add larksuite/cli -y -g

# 验证安装
lark-cli --version
```

### 2. 官方 CLI 登录授权

```bash
# 登录飞书（会弹出浏览器扫码）
lark-cli auth login --recommend

# 验证登录状态
lark-cli auth status

# 测试获取数据
lark-cli calendar +agenda
```

### 3. 微元配置

**方式一：使用 GUI 配置（推荐）**

```bash
# 启动微元PC客户端
python start_gui.py

# 菜单：工具 → 配置管理
# 填写以下配置：
# - 飞书：App ID、App Secret
# - 企业微信：Corp ID、Agent ID、Corp Secret
# - AI：OpenAI API Key 或 通义千问 Key
```

**方式二：配置文件直接编辑**

```bash
# 编辑配置文件
vim ~/.weiyuan/config.json

# 填入以下内容：
{
  "feishu": {
    "app_id": "cli_xxxxx",
    "app_secret": "xxxxx"
  },
  "wechat_work": {
    "corp_id": "wwxxxxx",
    "corp_secret": "xxxxx",
    "agent_id": "1000001"
  },
  "ai": {
    "openai_api_key": "sk-xxxxx",
    "openai_base_url": "https://api.openai.com/v1"
  }
}
```

### 4. 准备素材文件

```bash
# 创建目录
mkdir -p ./videos ./images ./charts

# 准备一段通用宣传视频（用于抖音）
# 命名为：./videos/daily_promo.mp4

# 准备商品展示图片（用于小红书）
# 命名为：./images/product_showcase.png
```

---

## 🚀 使用步骤

### 步骤1：复制模板

```bash
# 使用模板创建流程
cd weiyuan
opencli rpa init 销售数据自动发布 -t complete_sales_auto_publish

# 或者手动复制
cp rpa/templates/complete_sales_auto_publish.yaml ./我的销售自动化.yaml
```

### 步骤2：修改配置

编辑流程文件，修改以下配置：

```yaml
variables:
  # 修改为实际的多维表格token和表ID
  feishu_app_token: "你的多维表格token"
  feishu_table_id: "你的表格ID"
  
  # 可选：修改定时发布时间
  publish_time: "09:30"
```

**如何获取多维表格token和表ID：**

1. 打开飞书多维表格
2. 点击右上角 "..." → 打开方式 → 多维表格
3. 从浏览器地址栏复制 token（https://xxx.feishu.cn/base/**token**?table=**table_id**）

### 步骤3：测试执行

```bash
# 手动执行一次测试
opencli rpa run 我的销售自动化.yaml

# 或使用GUI执行
python start_gui.py
# 在流程管理页面找到流程，点击"执行"
```

**首次执行会要求：**
1. 扫码登录抖音（保存cookies）
2. 扫码登录小红书（保存cookies）

### 步骤4：设置定时任务

流程中已经设置了每天早上9点自动执行：

```yaml
trigger:
  type: schedule
  cron: "0 9 * * *"  # 每天早上9点
```

**添加系统定时任务：**

```bash
# 编辑crontab
crontab -e

# 添加以下行（每天早上8:50执行）
50 8 * * * cd /path/to/weiyuan && /usr/bin/python3 opencli rpa run 我的销售自动化.yaml >> /tmp/sales_auto.log 2>&1
```

---

## 📊 执行效果预览

### 1. 飞书获取的数据示例

```json
{
  "records": [
    {
      "商品名称": "智能手环",
      "销售额": 15000,
      "订单数": 30,
      "日期": "2024-03-30"
    },
    {
      "商品名称": "蓝牙耳机",
      "销售额": 23000,
      "订单数": 46,
      "日期": "2024-03-30"
    }
  ]
}
```

### 2. AI生成的抖音文案示例

```
🔥 今日销售破纪录！姐妹们太给力了！

智能手环、蓝牙耳机直接卖爆💥
销售额突破 ¥38,000！
库存告急，手慢无！👇

点击主页链接抢购！
#好物推荐 #今日热销 #智能穿戴
```

### 3. 企业微信通知示例

```
📊 每日销售数据日报

📈 核心指标
总销售额：¥38,000
订单数：76单
客单价：¥500

📱 自动化执行结果
✅ 抖音：已发布
✅ 小红书：已发布
✅ 数据图表：已生成
```

---

## 🔧 自定义配置

### 修改AI模型

```yaml
# 使用OpenAI GPT-4（效果更好但贵）
- name: AI生成文案
  uses: ai/llm@1.0.0
  with:
    provider: openai
    model: gpt-4

# 或使用通义千问（国产，便宜）
- name: AI生成文案
  uses: ai/llm@1.0.0
  with:
    provider: qwen
    model: qwen-plus
```

### 修改发布时间

```yaml
variables:
  publish_time: "18:00"  # 改为晚上6点发布
```

### 添加更多发布平台

```yaml
# 在步骤7后添加视频号发布
- name: 发布到视频号
  uses: publish/content@1.0.0
  with:
    platform: wechat_channel
    title: "今日销售战报"
    content: "..."
    files: ["./videos/daily_promo.mp4"]
```

### 修改飞书查询条件

```yaml
# 查询特定品类数据
params:
  filter: |
    {
      "conjunction": "and",
      "conditions": [
        {"field_name": "日期", "operator": "is", "value": ["${{ today() }}"]},
        {"field_name": "品类", "operator": "is", "value": ["电子产品"]}
      ]
    }
```

---

## ❓ 常见问题

### Q1: 官方CLI报错"未登录"？

```bash
# 重新登录
lark-cli auth login --recommend

# 检查状态
lark-cli auth status
```

### Q2: 抖音/小红书发布失败？

**原因**：cookies过期或首次使用

**解决**：
1. 手动执行一次流程
2. 按提示扫码登录
3. cookies会自动保存，下次无需再扫

### Q3: AI生成文案失败？

**检查**：
```bash
# 检查AI配置
cat ~/.weiyuan/config.json | grep -A5 ai

# 确保配置了有效的API Key
```

### Q4: 飞书获取不到数据？

**检查**：
1. 确认app_token和table_id正确
2. 确认多维表格中有"日期"、"销售额"等字段
3. 确认今日有数据

```bash
# 测试官方CLI能否获取数据
lark-cli base tables list --params '{"app_token":"你的token"}'
```

---

## 🎁 进阶玩法

### 玩法1：多账号矩阵发布

```yaml
# 同时发布到多个抖音账号
steps:
  - name: 发布到抖音账号1
    uses: publish/content@1.0.0
    with:
      cookies_path: "~/.weiyuan/douyin_account1.json"
  
  - name: 发布到抖音账号2
    uses: publish/content@1.0.0
    with:
      cookies_path: "~/.weiyuan/douyin_account2.json"
```

### 玩法2：根据销售额发送不同通知

```yaml
steps:
  - name: 判断是否破纪录
    uses: data/process@1.0.0
    with:
      action: condition
      condition: "${{ steps.计算汇总.output.total_sales > 50000 }}"
    register: is_record

# 破纪录发大红包通知
- name: 破纪录通知
  if: "${{ steps.判断是否破纪录.output.result }}"
  uses: wechat/work@1.0.0
  with:
    content: "🎉🎉🎉 破纪录啦！销售额突破5万！"
```

### 玩法3：周报表自动生成

```yaml
# 修改定时为每周一
trigger:
  cron: "0 9 * * 1"  # 每周一早上9点

steps:
  - name: 获取本周数据
    uses: lark/cli@1.0.0
    with:
      params:
        filter: "本周"
```

---

**这个完整场景展示了微元 + 官方CLI结合的强大能力！**
- 官方CLI：获取最全的飞书数据
- 微元：AI处理 + 跨平台发布 + 流程编排

**有任何问题随时问我！** 🦞
