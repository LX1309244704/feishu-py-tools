# 飞书Python工具箱 v1.1.0 发布说明

## 🎉 版本信息

- **版本号**：v1.1.0
- **发布日期**：2026-03-29
- **发布类型**：功能增强
- **GitHub地址**：https://github.com/LX1309244704/weiyuan

---

## 🚀 新增功能

### 1. 日历管理模块（CalendarManager）

**文件**：`feishu_core/calendar_manager.py`

**核心功能（8个）**：
- ✅ `get_primary_calendar()` - 获取主日历
- ✅ `list_calendars()` - 列出所有日历
- ✅ `get_calendar(calendar_id)` - 获取指定日历
- ✅ `create_calendar(name, description, color)` - 创建日历
- ✅ `create_event()` - 创建日程
- ✅ `get_event()` - 获取日程详情
- ✅ `list_events()` - 列出日程
- ✅ `update_event()` - 更新日程
- ✅ `delete_event()` - 删除日程
- ✅ `get_free_busy()` - 查询用户忙闲状态
- ✅ `search_events()` - 搜索日程

**使用示例**：
```python
from feishu_core.calendar_manager import CalendarManager

manager = CalendarManager(app_id="cli_xxx", app_secret="xxx")

# 创建日程
event_id = manager.create_event(
    calendar_id="cal_xxx",
    title="项目会议",
    start_time="2026-03-30T14:00:00+08:00",
    end_time="2026-03-30T15:00:00+08:00",
    description="讨论项目进度和下一步计划",
    attendees=[
        {"assignee_type": "user", "id": "ou_xxx"}
    ]
)

# 查询忙闲状态
free_busy = manager.get_free_busy(
    user_ids=["ou_xxx", "ou_yyy"],
    start_time="2026-03-30T00:00:00+08:00",
    end_time="2026-03-30T23:59:59+08:00"
)
```

---

### 2. 任务管理模块（TaskManager）

**文件**：`feishu_core/task_manager.py`

**核心功能（7个）**：
- ✅ `get_tasklists()` - 获取任务清单列表
- ✅ `create_tasklist()` - 创建任务清单
- ✅ `get_tasklist()` - 获取任务清单详情
- ✅ `create_task()` - 创建任务
- ✅ `get_task()` - 获取任务详情
- ✅ `list_tasks()` - 获取任务列表
- ✅ `update_task()` - 更新任务
- ✅ `delete_task()` - 删除任务
- ✅ `create_subtask()` - 创建子任务
- ✅ `get_subtasks()` - 获取子任务列表
- ✅ `search_tasks()` - 搜索任务
- ✅ `add_task_comment()` - 添加任务评论
- ✅ `get_task_comments()` - 获取任务评论

**使用示例**：
```python
from feishu_core.task_manager import TaskManager

manager = TaskManager(app_id="cli_xxx", app_secret="xxx")

# 创建任务清单
tasklist_id = manager.create_tasklist("项目任务清单", "项目开发任务")

# 创建任务
task_id = manager.create_task(
    tasklist_guid=tasklist_id,
    summary="开发用户管理系统",
    description="完成用户管理系统的开发和测试",
    due_time="2026-04-30T18:00:00+08:00",
    assignee="ou_xxx"
)

# 创建子任务
subtask_id = manager.create_subtask(
    parent_task_guid=task_id,
    summary="设计数据库表结构",
    description="设计用户、角色、权限等数据表"
)

# 添加评论
comment_id = manager.add_task_comment(
    task_guid=task_id,
    content="任务进展顺利，预计按时完成"
)
```

---

### 3. 消息管理模块（MessageManager）

**文件**：`feishu_core/message_manager.py`

**核心功能（10个）**：
- ✅ `send_text_message()` - 发送文本消息
- ✅ `send_card_message()` - 发送卡片消息
- ✅ `send_image_message()` - 发送图片消息
- ✅ `send_file_message()` - 发送文件消息
- ✅ `send_rich_text_message()` - 发送富文本消息
- ✅ `reply_message()` - 回复消息
- ✅ `get_message()` - 获取消息详情
- ✅ `get_chat_history()` - 获取聊天记录
- ✅ `delete_message()` - 删除消息
- ✅ `recall_message()` - 撤回消息
- ✅ `create_notification_card()` - 创建通知卡片
- ✅ `send_notification()` - 发送通知

**使用示例**：
```python
from feishu_core.message_manager import MessageManager

manager = MessageManager(app_id="cli_xxx", app_secret="xxx")

# 发送文本消息
msg_id = manager.send_text_message(
    receive_id="ou_xxx",
    content="您好！项目进度已完成80%"
)

# 发送卡片消息
card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {
            "content": "项目通知",
            "tag": "plain_text"
        }
    },
    "elements": [
        {
            "tag": "div",
            "text": {
                "content": "项目进度更新：当前已完成80%",
                "tag": "lark_md"
            }
        }
    ]
}
msg_id = manager.send_card_message("ou_xxx", card)

# 发送通知消息
manager.send_notification(
    receive_id="ou_xxx",
    title="任务提醒",
    content="您有一个任务即将到期",
    buttons=[
        {"text": "查看详情", "url": "https://example.com"},
        {"text": "完成任务", "url": "https://example.com/complete"}
    ]
)
```

---

## 📊 功能统计

### 模块数量
- **v1.0.0**：3个模块（Bitable、Doc、Config）
- **v1.1.0**：5个模块（新增Calendar、Task、Message）
- **增长**：+67%

### 功能数量
- **v1.0.0**：21个核心功能
- **v1.1.0**：46个核心功能
- **新增**：25个功能
- **增长**：+119%

### 代码统计
- **新增文件**：3个
- **新增代码**：1,254行
- **总代码行数**：3,600+行

---

## 💡 实际应用场景

### 场景1：项目会议管理

```python
from feishu_core.calendar_manager import CalendarManager
from feishu_core.task_manager import TaskManager

calendar = CalendarManager()
task = TaskManager()

# 安排项目会议
event_id = calendar.create_event(
    calendar_id="cal_xxx",
    title="项目周会",
    start_time="2026-03-30T14:00:00+08:00",
    end_time="2026-03-30T15:00:00+08:00",
    description="讨论本周项目进展",
    attendees=[
        {"assignee_type": "user", "id": "ou_xxx"},
        {"assignee_type": "user", "id": "ou_yyy"}
    ]
)

# 创建会议任务
task_id = task.create_task(
    tasklist_guid="tasklist_xxx",
    summary="准备周会PPT",
    description="准备项目周会的演示文稿",
    due_time="2026-03-30T12:00:00+08:00"
)

# 发送通知
manager = MessageManager()
manager.send_notification(
    receive_id="ou_xxx",
    title="会议提醒",
    content="明天14:00有项目周会，请提前准备"
)
```

### 场景2：任务跟踪与提醒

```python
from feishu_core.task_manager import TaskManager
from feishu_core.message_manager import MessageManager

task = TaskManager()
message = MessageManager()

# 创建任务
task_id = task.create_task(
    tasklist_guid="tasklist_xxx",
    summary="完成系统测试",
    description="完成所有模块的功能测试",
    due_time="2026-04-15T18:00:00+08:00",
    assignee="ou_xxx"
)

# 添加子任务
subtask1 = task.create_subtask(task_id, "单元测试")
subtask2 = task.create_subtask(task_id, "集成测试")

# 添加评论
task.add_task_comment(task_id, "测试进展顺利")

# 发送提醒
message.send_notification(
    receive_id="ou_xxx",
    title="任务提醒",
    content="您的任务\"完成系统测试\"即将到期"
)
```

### 场景3：团队协作通知

```python
from feishu_core.message_manager import MessageManager

manager = MessageManager()

# 发送团队通知
manager.send_notification(
    receive_id="oc_xxx",  # 群聊ID
    title="项目更新通知",
    content="v1.1.0版本已发布，包含日历、任务、消息管理模块",
    buttons=[
        {"text": "查看详情", "url": "https://github.com/LX1309244704/weiyuan"},
        {"text": "文档", "url": "https://github.com/LX1309244704/weiyuan/blob/main/EXAMPLES.md"}
    ]
)
```

---

## 🔧 技术改进

### 1. 模块化架构
- ✅ 独立的模块设计
- ✅ 统一的API调用方式
- ✅ 清晰的职责划分

### 2. 错误处理
- ✅ 统一的错误返回格式
- ✅ 详细的错误提示
- ✅ 异常捕获和处理

### 3. 代码质量
- ✅ 完整的类型注解
- ✅ 详细的文档字符串
- ✅ 清晰的函数命名

---

## 📚 文档更新

### 新增文档
- ✅ CHANGELOG.md - v1.1.0更新日志
- ✅ README.md - 更新功能模块说明

### 更新文档
- ✅ EXAMPLES.md - 添加新模块使用示例
- ✅ 开发路线图更新

---

## 🎯 下一步计划（v1.2.0）

### 计划功能
- [ ] AI集成模块（Claude、GPT、DeepSeek）
- [ ] 自然语言查询
- [ ] 智能推荐系统
- [ ] 数据清洗功能
- [ ] 工作流引擎基础

### 预计时间
- **开始时间**：2026-04-01
- **预计完成**：2026-04-15

---

## 🤝 贡献者

- **三金的小虾米** - 核心开发者

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **GitHub仓库**：https://github.com/LX1309244704/weiyuan
- **v1.1.0发布**：https://github.com/LX1309244704/weiyuan/releases/tag/v1.1.0
- **使用文档**：https://github.com/LX1309244704/weiyuan/blob/main/EXAMPLES.md
- **更新日志**：https://github.com/LX1309244704/weiyuan/blob/main/CHANGELOG.md

---

## 💬 反馈与支持

- **问题反馈**：https://github.com/LX1309244704/weiyuan/issues
- **功能建议**：https://github.com/LX1309244704/weiyuan/discussions
- **邮箱联系**：1309244704@qq.com

---

**🦞 感谢使用飞书Python工具箱！**

**v1.1.0版本带来了完整的日历、任务、消息管理功能，让飞书管理更加全面！**
