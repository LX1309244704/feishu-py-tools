# 微元 Weiyuan - 全生态RPA自动化平台

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/RPA-Automation-green.svg" alt="RPA">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Version-2.0.0-brightgreen.svg" alt="Version">
</p>

<p align="center">
  <b>一站式全生态RPA自动化平台</b><br>
  低代码 · 全生态 · AI增强 · 官方CLI集成 · 开箱即用
</p>

---

## 🚀 项目简介

**微元（Weiyuan）** 是一个功能强大的全生态RPA（机器人流程自动化）平台，让你通过简单的YAML配置，就能实现跨平台的自动化操作。无需编程基础，复制模板即可使用。

### ✨ 为什么选择微元？

| 特性 | 传统RPA工具 | 微元 |
|------|------------|------|
| 学习成本 | 需要编程基础 | 🟢 YAML配置，零代码 |
| 生态覆盖 | 单一平台 | 🟢 飞书+微信+抖音+小红书 |
| AI能力 | 无或弱 | 🟢 内置OCR+大模型（GPT/Claude/千问） |
| API覆盖 | 有限 | 🟢 官方CLI集成（2500+飞书API） |
| 使用方式 | 命令行 | 🟢 CLI+PC客户端+Web控制台 |
| 价格 | 付费订阅 | 🟢 完全免费开源 |

---

## 🎯 核心能力

### 1️⃣ RPA流程引擎
- ✅ **低代码流程定义**：YAML格式，5分钟上手
- ✅ **多维度触发**：定时、Webhook、事件、手动、条件触发
- ✅ **可视化执行**：实时日志、步骤追踪、错误重试
- ✅ **数据传递**：步骤间上下文自动传递，支持变量和表达式
- ✅ **变量引擎**：内置函数（日期、字符串、JSON处理）

### 2️⃣ 全生态插件（已内置15个）

#### 💼 飞书生态（3个插件）
| 插件 | 功能 |
|------|------|
| `feishu/bitable` | 多维表格：增删改查、批量导入导出 |
| `feishu/message` | 消息：文本/图片/卡片发送 |
| `feishu/doc` | 文档：创建、读取、更新、导出 |

#### 🚀 官方CLI集成（2个插件）⭐ NEW
| 插件 | 功能 |
|------|------|
| `lark/cli` | 官方CLI：快捷命令、API命令、通用API调用 |
| `lark/skill` | 官方Skill：调用飞书官方AI Agent |

**官方CLI优势：**
- 🎯 **200+精选命令**，自动同步官方API
- 🎯 **2500+API覆盖**，支持所有飞书功能
- 🎯 **19个AI Agent**，开箱即用

#### 💬 微信全生态（4个插件）
| 插件 | 功能 |
|------|------|
| `wechat/message` | 个人微信：给好友/群发消息、文件、图片 |
| `wechat/work` | 企业微信：内部消息、客户联系、外部客户群发 |
| `wechat/mp` | 公众号：模板消息、客服消息、粉丝管理 |
| `wechat/contact` | 客户联系：联系人管理、标签管理 |

#### 📱 内容平台（1个插件）
| 插件 | 功能 |
|------|------|
| `publish/content` | 小红书/抖音/视频号：一键发布图文/视频 |

#### 🖥️ UI自动化（2个插件）
| 插件 | 功能 |
|------|------|
| `ui/desktop` | 桌面自动化：鼠标/键盘、截图、图像识别 |
| `ui/browser` | 浏览器自动化：网页操作、元素定位、表单填写 |

#### 🤖 AI增强（2个插件）
| 插件 | 功能 |
|------|------|
| `ai/ocr` | OCR识别：图片/截图文字提取，支持中英文 |
| `ai/llm` | 大模型：GPT/Claude/通义千问，文本生成、摘要、翻译 |

#### 🛠️ 基础工具（2个插件）
| 插件 | 功能 |
|------|------|
| `data/process` | 数据处理：过滤、排序、聚合、Excel/CSV处理 |
| `file/operation` | 文件操作：读写、复制、移动、批量处理 |

### 3️⃣ 多端使用方式

#### 🖥️ PC客户端（推荐）
```bash
python start_gui.py
```
- 🎨 图形化配置界面
- 📊 实时执行监控
- 📋 流程可视化管理
- ⚙️ 无需命令行操作

#### 🌐 Web控制台
```bash
python -m rpa web
# 打开 http://localhost:8888
```
- 📱 浏览器访问，支持手机端
- 👥 适合团队协作
- 📈 执行历史和统计

#### ⌨️ CLI命令行
```bash
python -m rpa run my_flow.yaml
```
- 🚀 批量执行和自动化调度
- 🔄 集成到CI/CD
- 💻 适合技术人员

---

## 📦 快速开始

### 1. 安装（推荐方式）

```bash
# 克隆项目
git clone https://github.com/LX1309244704/weiyuan.git
cd weiyuan

# 安装核心依赖（最小化安装）
pip install click requests python-dotenv pyyaml rich jsonschema jinja2 lark-oapi flask gunicorn apscheduler

# 可选：安装GUI客户端
pip install PySide6

# 可选：安装官方CLI（需要Node.js）
npm install -g @larksuite/cli
lark-cli auth login --recommend
```

**详细安装指南：** [INSTALLATION.md](INSTALLATION.md) | [QUICK_INSTALL.md](QUICK_INSTALL.md)

### 2. 第一个RPA流程

创建 `hello.yaml`：
```yaml
name: 我的第一个RPA流程
steps:
  - name: 发送消息到企业微信
    uses: wechat/work@1.0.0
    with:
      action: send_text
      corp_id: "你的企业ID"
      corp_secret: "你的Secret"
      agent_id: 1000001
      receiver: "@all"
      content: "🎉 我的第一个RPA流程运行成功！"
```

执行：
```bash
python -m rpa run hello.yaml
```

### 3. 使用内置模板

```bash
# 查看所有模板
python -m rpa --help

# 使用模板创建流程
python -m rpa init 我的流程 -t wechat_send_message
python -m rpa init 销售报表 -t daily_sales_report
python -m rpa init 库存预警 -t inventory_alert
python -m rpa init 多平台发布 -t multi_platform_publish
python -m rpa init 官方CLI演示 -t lark_cli_weiyuan_demo
python -m rpa init 完整自动化 -t complete_sales_auto_publish
```

---

## 💡 典型使用场景

### 场景1：飞书+微信数据联动（官方CLI）

```yaml
name: 飞书数据自动同步到微信

steps:
  # 使用官方CLI获取飞书数据
  - name: 获取今日日程
    uses: lark/cli@1.0.0
    with:
      command: shortcut
      service: calendar
      shortcut: +agenda
    register: calendar_data
  
  # 处理数据
  - name: 生成报告
    uses: data/process@1.0.0
    with:
      action: format
      data: "${{ steps.获取今日日程.output.stdout }}"
  
  # 发送到微信群
  - name: 发送到微信群
    uses: wechat/message@1.0.0
    with:
      receiver: "业务群"
      msg_type: text
      content: "${{ steps.生成报告.output.formatted }}"
```

### 场景2：完整销售自动化（AI+多平台）

```yaml
name: 销售数据自动发布到抖音和微信

trigger:
  type: schedule
  cron: "0 9 * * *"  # 每天早上9点

steps:
  # 1. 官方CLI获取销售数据
  - name: 获取销售数据
    uses: lark/cli@1.0.0
    with:
      command: api
      service: base
      method: records/list
      params:
        app_token: "${{ env.FEISHU_APP_TOKEN }}"
    register: sales_data
  
  # 2. AI生成抖音文案
  - name: AI生成文案
    uses: ai/llm@1.0.0
    with:
      action: generate
      prompt: "根据以下数据生成抖音文案：${{ steps.获取销售数据.output.json }}"
    register: douyin_content
  
  # 3. 发布到抖音
  - name: 发布到抖音
    uses: publish/content@1.0.0
    with:
      platform: douyin
      content: "${{ steps.AI生成文案.output.content }}"
      files: ["./视频.mp4"]
  
  # 4. 发送企业微信通知
  - name: 发送通知
    uses: wechat/work@1.0.0
    with:
      action: send_markdown
      receiver: "运营部"
      content: "今日销售数据已发布到抖音"
```

### 场景3：自动截图识别

```yaml
steps:
  - name: 截图
    uses: ui/desktop@1.0.0
    with:
      action: screenshot
      save_path: "./screenshot.png"
  
  - name: OCR识别
    uses: ai/ocr@1.0.0
    with:
      action: recognize
      image_path: "./screenshot.png"
    register: ocr_result
  
  - name: 保存到飞书
    uses: feishu/bitable@1.0.0
    with:
      action: create_record
      app_token: "xxx"
      table_id: "xxx"
      fields:
        "内容": "${{ steps.OCR识别.output.full_text }}"
```

---

## 📁 项目结构

```
weiyuan/
├── 📄 README.md                 # 项目说明（本文件）
├── 📦 requirements*.txt         # 依赖文件（多种安装方式）
├── 🚀 start_gui.py             # 启动PC客户端
├── 🐳 Dockerfile               # Docker部署
│
├── rpa/                        # RPA核心代码
│   ├── core/                   # 核心引擎
│   │   ├── engine.py          # 执行引擎
│   │   ├── flow.py            # 流程解析
│   │   ├── plugin.py          # 插件系统
│   │   └── variable_engine.py # 变量引擎
│   ├── plugins/               # 插件集合（15个）
│   │   ├── feishu_plugins.py  # 飞书插件
│   │   ├── wechat_plugins.py  # 微信全生态
│   │   ├── lark_cli_plugin.py # 官方CLI集成 ⭐
│   │   ├── ui_plugins.py      # UI自动化
│   │   ├── ocr_plugin.py      # OCR识别
│   │   ├── ai_plugin.py       # AI大模型
│   │   └── publish_plugins.py # 内容发布
│   ├── templates/             # 流程模板（8个）
│   │   ├── wechat_send_message.yaml
│   │   ├── inventory_alert.yaml
│   │   ├── daily_sales_report.yaml
│   │   ├── multi_platform_publish.yaml
│   │   ├── lark_cli_weiyuan_demo.yaml
│   │   └── complete_sales_auto_publish.yaml
│   ├── cli/                   # 命令行工具
│   ├── gui/                   # PC客户端（6个页面）
│   └── web/                   # Web控制台
│
├── docs/                      # 详细文档
│   ├── LARK_CLI_INTEGRATION.md # 官方CLI集成指南
│   ├── COMPLETE_DEMO_GUIDE.md  # 完整演示指南
│   └── TUTORIAL_WITH_SCREENS.md # 带截图的教程
│
├── INSTALLATION.md            # 安装指南
├── QUICK_INSTALL.md           # 快速安装
├── BUG_FIXES.md              # Bug修复文档
└── DELIVERY_REPORT.md        # 项目交付报告
```

---

## 📖 完整文档

### 核心文档
| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目说明（本文件） |
| [INSTALLATION.md](INSTALLATION.md) | 详细安装指南 |
| [QUICK_INSTALL.md](QUICK_INSTALL.md) | 分步安装指南（推荐） |
| [BUG_FIXES.md](BUG_FIXES.md) | 已知问题和修复 |

### 功能文档
| 文档 | 说明 |
|------|------|
| [README_RPA.md](README_RPA.md) | RPA工具完整使用指南 |
| [README_GUI.md](README_GUI.md) | PC客户端使用指南 |
| [README_DEPLOY.md](README_DEPLOY.md) | 部署指南（Docker/Railway/Render） |
| [README_COZE.md](README_COZE.md) | 扣子平台部署指南 |

### 深度教程
| 文档 | 说明 |
|------|------|
| [docs/LARK_CLI_INTEGRATION.md](docs/LARK_CLI_INTEGRATION.md) | 官方CLI集成指南 |
| [docs/COMPLETE_DEMO_GUIDE.md](docs/COMPLETE_DEMO_GUIDE.md) | 完整实战演示 |
| [docs/TUTORIAL_WITH_SCREENS.md](docs/TUTORIAL_WITH_SCREENS.md) | 带截图的详细教程 |

---

## 🛣️ 开发路线图

### ✅ v1.0.0 已完成
- [x] RPA核心引擎
- [x] 飞书生态插件
- [x] 微信个人插件
- [x] PC客户端

### ✅ v2.0.0 已完成（当前版本）
- [x] 企业微信插件
- [x] 公众号插件
- [x] UI自动化插件
- [x] OCR插件
- [x] AI大模型插件
- [x] Web控制台
- [x] 内容发布插件（小红书/抖音/视频号）
- [x] **官方CLI集成**（2500+飞书API）
- [x] 完整文档体系

### 📅 v3.0.0 计划中
- [ ] 更多内容平台（B站/知乎/微博）
- [ ] 数据库插件（MySQL/PostgreSQL/MongoDB）
- [ ] 邮件插件（SMTP/IMAP）
- [ ] 定时任务调度优化
- [ ] 云端托管版本

---

## 🐛 已修复问题

| 问题 | 状态 | 详情 |
|------|------|------|
| GUI启动错误 | ✅ 已修复 | QLabel导入缺失 |
| lark-cli-wrapper不存在 | ✅ 已修复 | 改用npm安装官方CLI |
| concurrent-futures不存在 | ✅ 已修复 | Python标准库，无需安装 |
| 编码错误 | ✅ 已修复 | 中文注释改英文 |
| 类型注解缺失 | ✅ 已修复 | 添加Dict/Any/List导入 |

**详细修复记录：** [BUG_FIXES.md](BUG_FIXES.md)

---

## 🤝 贡献指南

欢迎贡献代码！无论是：
- 🐛 修复Bug
- ✨ 新增插件
- 📖 完善文档
- 💡 提出建议

请查看 [贡献指南](CONTRIBUTING.md)。

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👥 关于作者

- **作者**：三金的小虾米
- **邮箱**：1309244704@qq.com
- **GitHub**：https://github.com/LX1309244704
- **项目主页**：https://github.com/LX1309244704/weiyuan

---

## 🙏 致谢

- [飞书官方CLI](https://github.com/larksuite/cli) - 强大的命令行工具
- [PySide6](https://www.qt.io/) - 优秀的GUI框架
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - 优秀的OCR引擎

---

## 📞 联系我们

- 🐛 **Bug报告**：[GitHub Issues](https://github.com/LX1309244704/weiyuan/issues)
- 💬 **问题讨论**：[GitHub Discussions](https://github.com/LX1309244704/weiyuan/discussions)
- 📧 **邮件联系**：1309244704@qq.com

---

<p align="center">
  <b>🦞 微元 Weiyuan - 让自动化触手可及！</b>
  <br>
  <sub>⭐ 如果觉得有用，请给我们一个Star！</sub>
</p>
