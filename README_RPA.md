# 🤖 RPA工具使用指南
基于opencli/飞书Python工具箱的机器人流程自动化工具，让你可以通过低代码的方式自动化办公流程。

---

## ✨ 核心特性
- **低代码流程定义**：YAML/JSON格式，无需写代码
- **丰富插件生态**：飞书操作、数据处理、文件操作、HTTP请求等
- **多维度触发**：定时、Webhook、事件、手动、条件触发
- **变量系统**：支持上下文传递、表达式计算、内置函数
- **企业级能力**：错误重试、超时控制、失败回调、日志审计
- **CLI命令行**：简单易用的命令行工具

---

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements_rpa.txt
```

### 2. 创建第一个RPA流程
```bash
# 创建流程模板
opencli rpa init 库存预警流程
```

会生成`inventory_alert_flow.yaml`文件，编辑配置你的流程逻辑。

### 3. 验证流程格式
```bash
opencli rpa validate inventory_alert_flow.yaml
```

### 4. 执行流程
```bash
opencli rpa run inventory_alert_flow.yaml

# 带上下文参数执行
opencli rpa run inventory_alert_flow.yaml -c '{"custom_param": "value"}'

# 保存执行结果
opencli rpa run inventory_alert_flow.yaml -o result.json
```

---

## 📖 流程定义语法

### 基础结构
```yaml
# 流程基本信息
name: 流程名称
description: 流程描述
version: 1.0.0

# 触发条件
trigger:
  type: manual  # 触发类型：manual/schedule/webhook/event/condition
  cron: "0 18 * * 1-5"  # 定时触发时填写Cron表达式

# 全局变量
variables:
  app_id: "cli_xxxxxx"
  app_secret: "xxxxxx"

# 步骤列表
steps:
  - name: 步骤名称
    uses: 插件名@版本  # 比如feishu/bitable@1.0.0
    with:  # 插件参数
      action: list_tables
      app_token: "${{ globals.app_token }}"  # 引用全局变量
      app_id: "${{ globals.app_id }}"
    if: "${{ 条件表达式 }}"  # 可选：满足条件才执行
    timeout: 300  # 可选：超时时间，默认300秒
    retry: 2  # 可选：失败重试次数，默认0
    continue_on_failure: false  # 可选：失败是否继续，默认false

# 执行成功回调（可选）
on_success:
  - name: 成功通知
    uses: feishu/message@1.0.0
    with:
      receive_id: "ou_xxxxxx"
      content: "流程执行成功！"

# 执行失败回调（可选）
on_failure:
  - name: 失败告警
    uses: feishu/message@1.0.0
    with:
      receive_id: "ou_xxxxxx"
      content: "流程执行失败！错误：${{ error }}"

# 流程设置（可选）
settings:
  log_level: info  # 日志级别：debug/info/warn/error
  timeout: 3600  # 总流程超时时间，默认3600秒
  max_parallel: 1  # 最大并行执行数
```

### 变量和表达式
使用 `${{ 表达式 }}` 语法引用变量和计算：

#### 内置变量
- `${{ globals.xxx }}`：全局变量
- `${{ steps.步骤名.output.xxx }}`：前面步骤的输出结果
- `${{ env.xxx }}`：环境变量
- `${{ flow.xxx }}`：流程元数据
- `${{ error }}`：错误信息（仅在on_failure中可用）

#### 内置函数
- `now()`：当前时间
- `today(format='%Y-%m-%d')`：当前日期
- `len(obj)`：获取长度
- `sum(list)`：求和
- `max(list)`：最大值
- `min(list)`：最小值
- `upper(str)`：转大写
- `lower(str)`：转小写
- `json_dumps(obj)`：JSON序列化
- `json_loads(str)`：JSON反序列化

#### 示例
```yaml
# 引用步骤结果
app_token: "${{ steps.获取配置.output.app_token }}"

# 表达式计算
if: "${{ len(steps.拉取数据.output.data) > 0 }}"

# 使用内置函数
content: "今日日期：{{ today('%Y年%m月%d日') }}"
```

---

## 🔌 内置插件列表

### 飞书生态插件
| 插件名 | 功能 |
|--------|------|
| `feishu/bitable@1.0.0` | 多维表格操作：增删改查、导入导出 |
| `feishu/message@1.0.0` | 消息发送：文本、富文本、卡片、文件 |
| `feishu/doc@1.0.0` | 文档操作：创建、读取、更新、导出 |

### 基础插件
| 插件名 | 功能 |
|--------|------|
| `data/process@1.0.0` | 数据处理：过滤、排序、聚合、转换、去重 |
| `file/operation@1.0.0` | 文件操作：读写、复制、移动、删除、CSV/Excel处理 |
| `http/request@1.0.0` | HTTP请求：GET/POST/PUT/DELETE，支持JSON/表单 |

---

## 📝 模板示例

### 1. 库存预警流程
`rpa/templates/inventory_alert.yaml`
- 每2小时检查一次库存
- 低于最小库存时发送预警通知
- 失败自动告警

### 2. 每日销售报表流程
`rpa/templates/daily_sales_report.yaml`
- 工作日18点自动执行
- 统计当日销售数据
- 生成Excel报表并发送群通知

---

## 🛠️ CLI命令参考

### 执行流程
```bash
opencli rpa run <流程文件> [选项]
选项：
  -c, --context TEXT  上下文JSON字符串
  -o, --output TEXT   结果输出文件路径
```

### 验证流程
```bash
opencli rpa validate <流程文件>
```

### 列出所有流程
```bash
opencli rpa list
```

### 创建新流程模板
```bash
opencli rpa init <流程名称> [选项]
选项：
  -d, --description TEXT  流程描述
```

### 插件管理
```bash
# 列出所有已安装插件
opencli rpa plugin list
```

---

## 📊 典型应用场景

### 1. 业务自动化
- 库存预警、补货提醒
- 销售报表自动生成
- 考勤/绩效/报销自动提醒
- 审批流程自动通知

### 2. 数据同步
- 飞书多维表格 ↔ 业务系统数据同步
- 跨系统数据迁移
- 数据定时备份

### 3. 办公效率提升
- 新员工入职流程自动化
- 会议纪要自动整理
- 客户跟进自动提醒
- 报表自动汇总

---

## 🔧 开发自定义插件

### 步骤
1. 继承`BasePlugin`基类
2. 实现`execute`方法
3. 使用`@register_plugin`装饰器注册

### 示例
```python
from rpa.core.plugin import BasePlugin, register_plugin

@register_plugin
class MyPlugin(BasePlugin):
    plugin_name = "my/custom_plugin"
    plugin_version = "1.0.0"
    plugin_description = "我的自定义插件"
    plugin_author = "作者名"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        # 实现插件逻辑
        param1 = params.get('param1')
        return {
            'success': True,
            'result': '执行结果'
        }
```

---

## 📈 部署方式

### 本地运行
直接通过`opencli rpa run`命令执行，定时任务用系统Cron调度。

### 服务端部署
部署为后台服务，内置调度器，支持多流程管理和Web控制台（开发中）。

### 容器化部署
```dockerfile
FROM python:3.10-slim
RUN pip install opencli
COPY ./flows /app/flows
CMD ["opencli", "rpa", "server"]
```

---

## ❓ 常见问题

### Q: 如何调试流程？
A: 1. 使用`opencli rpa validate`先验证格式 2. 手动执行看日志 3. 调试时加上`-v`参数显示详细日志。

### Q: 如何处理敏感信息？
A: 敏感信息（比如app_secret）建议通过环境变量传入，不要写在流程文件里，`${{ env.APP_SECRET }}`可以读取环境变量。

### Q: 支持并行执行步骤吗？
A: 支持，在步骤配置里加上`parallel: true`即可并行执行。

---

## 🎯 下一步计划
- [ ] Web可视化流程编辑器
- [ ] 流程监控管理控制台
- [ ] 更多插件（浏览器自动化、OCR、AI增强）
- [ ] 分布式执行支持
- [ ] 流程市场、模板分享
