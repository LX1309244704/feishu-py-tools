# 🚀 飞书Python工具箱 - 扣子平台部署指南

## 📋 前置要求

- 扣子（Coze）账号：https://www.coze.cn
- GitHub账号（用于代码托管）
- 飞书应用权限

---

## 🌟 为什么选择扣子平台部署？

### ✅ 扣子平台优势

| 特性 | 扣子平台 | Railway/Render |
|------|---------|---------------|
| **AI集成** | ✅ 原生支持大模型 | ❌ 需要自己集成 |
| **自然语言开发** | ✅ 一句话生成 | ❌ 需要写代码 |
| **可视化编排** | ✅ 拖拽式工作流 | ❌ 需要编程 |
| **快速部署** | ✅ 一键部署 | ✅ 自动部署 |
| **多渠道发布** | ✅ 10+渠道 | ❌ 仅Web |
| **免费额度** | ✅ 充足 | ⚠️ 有限制 |
| **知识库** | ✅ 内置RAG | ❌ 无 |
| **插件生态** | ✅ 丰富插件 | ❌ 无 |
| **无需编程** | ✅ 低代码 | ❌ 需要Python |

---

## 🎯 部署方案对比

### 方案1：扣子应用（推荐）⭐

**适用场景**：AI应用、智能助手、对话式应用

**优点**：
- 🤖 原生AI能力集成
- 💬 自然语言对话
- 📚 内置知识库
- 🔌 丰富插件生态
- 📱 多平台发布（微信、抖音、飞书等）
- ⚡ 快速部署和迭代

**缺点**：
- 需要适配扣子平台架构
- 某些复杂功能需要自定义插件

### 方案2：扣子API服务

**适用场景**：需要API接口的应用

**优点**：
- 🔌 REST API接口
- 🔐 支持鉴权
- 📊 支持流式输出
- 🔧 灵活集成

**缺点**：
- 需要自己开发前端
- 需要处理API调用

---

## 📝 部署步骤

### 方案1：扣子应用部署

#### 步骤1：登录扣子平台

1. 访问 https://www.coze.cn
2. 使用手机号或邮箱注册/登录

#### 步骤2：创建应用项目

1. 点击左侧"工作空间"
2. 选择一个工作空间
3. 点击"创建" → "应用"
4. 选择"空白应用"
5. 输入应用信息：
   - **应用名称**：飞书Python工具箱
   - **应用描述**：飞书API封装工具，支持多维表格、文档、日历等
   - **图标**：点击AI图标自动生成
6. 点击"确定"

#### 步骤3：编排业务逻辑

##### 3.1 创建工作流

1. 在"业务逻辑"页面，找到"工作流"
2. 点击"+" → "新建工作流"
3. 输入工作流信息：
   - **工作流名称**：feishu_api
   - **描述**：飞书API调用工作流
4. 点击"确定"

##### 3.2 添加节点

工作流需要以下节点：

**开始节点**
- 配置输入参数：
  - `action`: 操作类型（如：get_tables、get_records、create_record）
  - `app_token`: 飞书应用Token
  - `table_id`: 表格ID（可选）
  - `fields`: 字段数据（可选）
  - `app_id`: 飞书应用ID
  - `app_secret`: 飞书应用密钥

**代码节点（Python）**

```python
async def main(args: Args) -> Output:
    params = args.params
    
    action = params.get('action')
    app_token = params.get('app_token')
    table_id = params.get('table_id')
    fields = params.get('fields', {})
    app_id = params.get('app_id')
    app_secret = params.get('app_secret')
    
    # 导入飞书SDK
    from lark_oapi.api.bitable.v1 import *
    
    # 初始化客户端
    client = Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .build()
    
    result = {}
    
    try:
        if action == 'get_tables':
            # 获取表格列表
            request = ListAppTableRequest.builder() \
                .app_token(app_token) \
                .build()
            response = client.bitable.v1.app_table.list(request)
            result = {
                'success': True,
                'data': response.data
            }
            
        elif action == 'get_records':
            # 获取记录列表
            request = ListAppTableRecordRequest.builder() \
                .app_token(app_token) \
                .table_id(table_id) \
                .build()
            response = client.bitable.v1.app_table_record.list(request)
            result = {
                'success': True,
                'data': response.data
            }
            
        elif action == 'create_record':
            # 创建记录
            request = CreateAppTableRecordRequest.builder() \
                .app_token(app_token) \
                .table_id(table_id) \
                .records([AppTableRecord.builder().fields(fields).build()]) \
                .build()
            response = client.bitable.v1.app_table_record.create(request)
            result = {
                'success': True,
                'data': response.data
            }
            
        else:
            result = {
                'success': False,
                'error': f'未知操作: {action}'
            }
            
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return result
```

**结束节点**
- 配置输出参数：
  - `result`: 代码节点返回的结果

##### 3.3 连接节点

1. 从开始节点连接到代码节点
2. 从代码节点连接到结束节点

##### 3.4 测试工作流

点击"试运行"按钮，输入测试参数：
```json
{
  "action": "get_tables",
  "app_token": "AXDyb30BNamJJ6sMYh2cda7Gnxg",
  "app_id": "cli_xxx",
  "app_secret": "xxx"
}
```

#### 步骤4：搭建用户界面

##### 4.1 创建H5页面

1. 点击"用户界面"页签
2. 选择"H5"
3. 点击"开始搭建"

##### 4.2 添加组件

**顶部标题**
- 组件：文本
- 内容：飞书Python工具箱

**应用操作区域**

**操作选择**
- 组件：下拉选择
- 选项：
  - 获取表格列表
  - 获取记录列表
  - 创建记录

**参数输入**
- 组件：输入框
- 字段1：App Token
- 字段2：Table ID
- 字段3：App ID
- 字段4：App Secret

**执行按钮**
- 组件：按钮
- 文本：执行
- 绑定事件：点击 → 调用工作流

**结果展示**
- 组件：文本/代码编辑器
- 绑定数据：工作流返回的result

##### 4.5 预览测试

点击"预览"按钮，测试完整流程：
1. 选择操作类型
2. 输入必要参数
3. 点击执行按钮
4. 查看结果

#### 步骤5：发布应用

##### 5.1 发布到扣子商店

1. 点击右上角"发布"按钮
2. 输入版本信息：
   - **版本号**：v1.0.0
   - **发布描述**：飞书Python工具箱初版
3. 选择发布渠道：
   - ✅ 扣子商店
   - ✅ 应用分类：工具类
4. 点击"发布"

##### 5.2 发布为Web应用

1. 在发布页面，选择"Web应用"
2. 配置域名：
   - 使用默认域名或自定义域名
3. 点击"发布"
4. 获取访问链接

**部署后的URL示例**：
```
https://feishu-tools.coze.cn/
```

##### 5.3 发布为API服务

1. 在发布页面，选择"API服务"
2. 配置API设置：
   - **鉴权方式**：Token
   - **配额限制**：1000次/小时
3. 点击"发布"
4. 获取API文档和Token

**API调用示例**：
```bash
curl -X POST https://api.coze.cn/open_api/v2/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "YOUR_BOT_ID",
    "user": "user_123",
    "query": "获取表格列表，app_token=AXDyb30BNamJJ6sMYh2cda7Gnxg",
    "stream": false
  }'
```

---

### 方案2：扣子API服务部署

#### 步骤1：创建智能体

1. 点击"创建" → "智能体"
2. 输入智能体信息：
   - **名称**：飞书Python工具箱Bot
   - **描述**：飞书API调用助手
   - **图标**：AI生成
3. 点击"确定"

#### 步骤2：编写提示词

在人设与回复逻辑中输入：

```
角色
你是一个飞书API调用助手，帮助用户操作飞书的多维表格、文档、日历等功能。

技能
技能1：多维表格操作
- 获取表格列表：根据app_token获取应用下的所有表格
- 获取记录列表：根据app_token和table_id获取表格记录
- 创建记录：在指定表格中创建新记录

技能2：文档操作
- 创建文档：创建新的飞书文档
- 获取文档：获取文档内容

技能3：日历操作
- 创建日程：在指定日历中创建日程
- 获取日程：获取日历中的日程

限制
- 只回答与飞书API相关的问题
- 需要提供有效的app_id、app_secret等凭证
- 对于敏感信息，提醒用户注意安全

回复示例
我可以帮你操作飞书的多维表格、文档、日历等。请告诉我你需要做什么，并提供必要的凭证信息。
```

#### 步骤3：添加技能（可选）

如果需要扩展功能，可以添加：
- **插件**：搜索、翻译、图片处理等
- **知识库**：飞书API文档、使用指南等
- **变量**：存储用户凭证、常用配置等

#### 步骤4：调试智能体

在预览区域测试：
- 用户：获取表格列表，app_token=AXDyb30BNamJJ6sMYh2cda7Gnxg
- 智能体：[返回表格列表]

#### 步骤5：发布为API

1. 点击右上角"发布"按钮
2. 选择"API"
3. 配置：
   - **Bot ID**：自动生成
   - **Access Token**：生成并保存（只显示一次！）
4. 点击"发布"

#### 步骤6：调用API

```python
from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL

# 初始化客户端
coze = Coze(
    auth=TokenAuth(token="YOUR_ACCESS_TOKEN"),
    base_url=COZE_CN_BASE_URL
)

# 调用智能体
response = coze.chat.chat(
    bot_id="YOUR_BOT_ID",
    user="user_123",
    query="获取表格列表，app_token=AXDyb30BNamJJ6sMYh2cda7Gnxg",
    stream=False
)

print(response)
```

---

## 🔧 高级功能

### 1. 使用扣子编程（一句话生成）

访问 https://code.coze.cn/

输入需求：
```
创建一个飞书多维表格管理应用，支持获取表格列表、查看记录、创建记录等功能
```

扣子会自动：
1. 分析需求
2. 匹配服务
3. 生成代码
4. 测试应用
5. 一键部署

### 2. 自定义插件

如果需要特定功能，可以创建自定义插件：

```python
async def main(args: Args) -> Output:
    params = args.params
    
    # 自定义逻辑
    result = {
        "success": True,
        "data": "自定义功能执行成功"
    }
    
    return result
```

### 3. 集成知识库

1. 准备飞书API文档
2. 在应用中创建知识库
3. 上传文档
4. 在智能体中使用知识库

---

## 📱 多渠道发布

扣子支持发布到多个平台：

### 1. 微信
- 发布为微信小程序
- 或通过API集成到微信客服

### 2. 抖音
- 发布为抖音小程序
- 集成到抖音企业号

### 3. 飞书
- 集成到飞书应用
- 作为飞书机器人

### 4. 豆包
- 发布到豆包智能体商店

### 5. 自定义域名
- 配置自定义域名
- 使用HTTPS

---

## 📊 与Railway/Render对比

| 特性 | 扣子平台 | Railway | Render |
|------|---------|---------|--------|
| **部署难度** | ⭐ 简单 | ⭐⭐ 中等 | ⭐⭐ 中等 |
| **AI能力** | ⭐⭐⭐⭐⭐ | ⭐⭐ 需要自己集成 | ⭐⭐ 需要自己集成 |
| **自然语言** | ⭐⭐⭐⭐⭐ | ❌ | ❌ |
| **可视化** | ⭐⭐⭐⭐⭐ | ❌ | ❌ |
| **多平台** | ⭐⭐⭐⭐⭐ 10+渠道 | ❌ 仅Web | ❌ 仅Web |
| **免费额度** | ⭐⭐⭐⭐⭐ 充足 | ⭐⭐⭐ 有限制 | ⭐⭐ 有限制 |
| **知识库** | ⭐⭐⭐⭐⭐ | ❌ | ❌ |
| **插件生态** | ⭐⭐⭐⭐⭐ | ❌ | ❌ |
| **适合场景** | AI应用 | 通用Web应用 | 通用Web应用 |

---

## 🎯 推荐选择

### 你的项目：飞书Python工具箱

**强烈推荐：扣子平台** ✅

**理由**：
1. 🤖 你是AI应用，扣子原生支持
2. 💬 需要自然语言对话，扣子内置
3. 📚 需要知识库存储文档，扣子支持
4. 🔌 需要插件扩展，扣子生态丰富
5. 📱 需要多平台发布，扣子支持10+渠道
6. ⚡ 快速迭代，扣子支持自然语言修改

---

## 📝 部署清单

### 扣子应用部署

- [ ] 注册扣子账号
- [ ] 创建应用项目
- [ ] 编排业务逻辑（工作流）
- [ ] 搭建用户界面
- [ ] 测试应用
- [ ] 发布到扣子商店
- [ ] 发布为Web应用
- [ ] 获取访问链接

### 扣子API服务部署

- [ ] 创建智能体
- [ ] 编写提示词
- [ ] 添加技能（可选）
- [ ] 调试智能体
- [ ] 发布为API
- [ ] 获取Access Token
- [ ] 集成到业务系统

---

## 🔗 相关链接

- **扣子官网**：https://www.coze.cn
- **扣子编程**：https://code.coze.cn
- **扣子文档**：https://www.coze.cn/docs
- **你的GitHub**：https://github.com/LX1309244704/weiyuan

---

## 🎉 总结

**扣子平台是飞书Python工具箱的最佳部署方案！**

### 优势
✅ 原生AI能力
✅ 自然语言开发
✅ 可视化编排
✅ 多渠道发布
✅ 免费额度充足
✅ 快速部署和迭代

### 下一步
1. 注册扣子账号
2. 创建应用项目
3. 开始编排业务逻辑
4. 一键部署上线

**需要我帮你详细指导扣子部署的某个步骤吗？** 🦞
