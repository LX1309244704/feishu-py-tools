# 🔗 微元 + 飞书官方 CLI 结合使用指南

## 🎯 结合方案概述

**最佳实践：官方 CLI 做飞书深度操作 + 微元做跨平台流程编排**

```
┌─────────────────────────────────────────────────────────────┐
│                      微元 Weiyuan 流程                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ 官方CLI插件   │    │  微元插件     │    │  微元插件     │  │
│  │ lark/cli     │ →  │ data/process │ →  │ wechat/work  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         ↓                   ↓                   ↓          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ 飞书官方CLI   │    │  数据处理     │    │  企业微信     │  │
│  │ (200+命令)   │    │  格式转换     │    │  消息发送     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📦 安装步骤

### 1. 安装官方 CLI

```bash
# 安装飞书官方 CLI
npm install -g @larksuite/cli

# 安装 CLI Skill（必需）
npx skills add larksuite/cli -y -g

# 验证安装
lark-cli --version
```

### 2. 配置认证

```bash
# 交互式登录
lark-cli auth login --recommend

# 或按业务域登录
lark-cli auth login --domain calendar,im,doc

# 查看登录状态
lark-cli auth status
```

### 3. 安装微元依赖

```bash
cd weiyuan
pip install -r requirements.txt
pip install -r requirements_rpa.txt
```

## 🚀 使用方式

### 方式一：在微元流程中调用官方 CLI

```yaml
steps:
  # 使用官方 CLI 获取飞书数据
  - name: 获取日程
    uses: lark/cli@1.0.0
    with:
      command: shortcut           # 快捷命令
      service: calendar           # 服务名
      shortcut: +agenda          # 快捷命令名
      format: json
    register: calendar_data
  
  # 使用微元发送到微信
  - name: 发送报告
    uses: wechat/work@1.0.0
    with:
      action: send_text
      content: "今日日程：${{ steps.获取日程.output.stdout }}"
```

### 方式二：使用官方 CLI API 命令

```yaml
steps:
  # 使用官方 CLI 的 API 命令（自动同步官方 API）
  - name: 获取多维表格数据
    uses: lark/cli@1.0.0
    with:
      command: api
      service: base
      method: tables/list
      params:
        app_token: "your_app_token"
    register: tables
```

### 方式三：使用官方 CLI Skill

```yaml
steps:
  # 调用官方 CLI Skill
  - name: 使用 Skill 发送消息
    uses: lark/skill@1.0.0
    with:
      skill: lark-im
      action: messages-send
      args:
        - "--chat-id=oc_xxx"
        - "--text=Hello from Skill"
```

## 📚 官方 CLI 命令类型

### 1. 快捷命令（Shortcuts）

微元插件参数：
```yaml
command: shortcut
service: <服务名>
shortcut: +<命令名>
params:
  <参数名>: <参数值>
```

示例命令：
- `calendar +agenda` - 查看日程
- `im +messages-send` - 发送消息
- `doc +create` - 创建文档
- `base +tables-list` - 列出多维表格

### 2. API 命令（API Commands）

微元插件参数：
```yaml
command: api
service: <服务名>
method: <方法名>
params: <请求参数>
```

示例命令：
- `calendar calendars list` - 列出日历
- `im messages list` - 列出消息
- `base tables list` - 列出表格

### 3. 通用 API 调用（Generic API）

微元插件参数：
```yaml
command: generic
http_method: GET/POST/PUT/DELETE
endpoint: /open-apis/xxx
params: <查询参数>
body: <请求体>
```

示例：
```yaml
- name: 调用任意 API
  uses: lark/cli@1.0.0
  with:
    command: generic
    http_method: GET
    endpoint: /open-apis/calendar/v4/calendars
```

## 💡 典型使用场景

### 场景1：飞书日程自动同步到微信

```yaml
name: 日程同步
steps:
  # 官方 CLI 获取日程（最全面的数据）
  - name: 获取日程
    uses: lark/cli@1.0.0
    with:
      command: shortcut
      service: calendar
      shortcut: +agenda
  
  # 微元处理并发送到微信
  - name: 发送微信
    uses: wechat/work@1.0.0
    with:
      action: send_markdown
      content: "${{ steps.获取日程.output.stdout }}"
```

### 场景2：飞书数据自动同步到抖音视频描述

```yaml
name: 数据到抖音
steps:
  # 官方 CLI 获取飞书数据
  - name: 获取销售数据
    uses: lark/cli@1.0.0
    with:
      command: api
      service: base
      method: records/search
      params:
        app_token: xxx
        table_id: xxx
  
  # 微元生成视频文案
  - name: 生成文案
    uses: ai/llm@1.0.0
    with:
      action: generate
      prompt: "根据以下数据生成抖音文案：${{ steps.获取销售数据.output.json }}"
  
  # 微元发布到抖音
  - name: 发布抖音
    uses: publish/content@1.0.0
    with:
      platform: douyin
      content: "${{ steps.生成文案.output.content }}"
```

## ⚠️ 注意事项

1. **官方 CLI 需要单独安装**
   - 微元不会自动安装官方 CLI
   - 需要手动运行 `npm install -g @larksuite/cli`

2. **认证状态共享**
   - 官方 CLI 的登录状态保存在系统密钥链
   - 微元调用时会使用已登录的账号

3. **输出格式**
   - 建议使用 `format: json` 获取结构化数据
   - 方便微元后续处理

4. **错误处理**
   - 官方 CLI 未安装时会返回友好提示
   - 建议在流程中添加错误处理

## 🎁 优势总结

| 能力 | 官方 CLI | 微元 | 结合使用 |
|------|---------|------|---------|
| 飞书API覆盖 | ⭐⭐⭐ 2500+ | ⭐⭐ 常用API | ⭐⭐⭐ 全覆盖 |
| API自动同步 | ⭐⭐⭐ 自动生成 | ❌ 手动开发 | ⭐⭐⭐ 享受同步 |
| 跨平台联动 | ❌ 仅飞书 | ⭐⭐⭐ 多平台 | ⭐⭐⭐ 飞书+微信+抖音 |
| 流程编排 | ❌ 单条命令 | ⭐⭐⭐ YAML编排 | ⭐⭐⭐ 完整流程 |
| 可视化 | ❌ 命令行 | ⭐⭐⭐ PC+Web | ⭐⭐⭐ 完整体验 |

**结合使用 = 享受官方 CLI 的全部能力 + 微元的跨平台自动化能力！** 🦞
