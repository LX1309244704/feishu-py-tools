

---

## 🌐 Web控制台使用指南
### 启动控制台
```bash
# 安装Web依赖
pip install flask flask-cors flask-socketio

# 启动服务
opencli rpa web
```
访问 http://localhost:8888 即可进入Web控制台。

### 功能模块
1. **仪表盘**：统计概览、最近执行记录
2. **流程管理**：流程列表、在线编辑、执行、删除
3. **执行记录**：历史执行记录、执行状态、日志查看
4. **模板市场**：内置模板列表，一键使用
5. **插件中心**：已安装插件列表
6. **系统设置**：配置管理

### 特色功能
- ✅ 在线YAML编辑器，语法高亮
- ✅ 实时验证流程格式
- ✅ 一键执行流程，实时查看日志
- ✅ 可视化界面，无需命令行操作
- ✅ 响应式设计，支持手机访问

---

## 🎯 UI自动化使用示例
### 桌面自动化：自动打开记事本输入文字
```yaml
steps:
  - name: 按下Win+R打开运行
    uses: ui/desktop@1.0.0
    with:
      action: hotkey
      keys: ["win", "r"]
  
  - name: 输入notepad并回车
    uses: ui/desktop@1.0.0
    with:
      action: type_text
      text: "notepad\n"
  
  - name: 等待记事本打开
    uses: ui/desktop@1.0.0
    with:
      action: wait_image
      image_path: "./notepad_icon.png"
      timeout: 5
  
  - name: 输入文字
    uses: ui/desktop@1.0.0
    with:
      action: type_text
      text: "这是RPA自动输入的文字！"
```

### 浏览器自动化：自动打开百度搜索
```yaml
steps:
  - name: 打开百度
    uses: ui/browser@1.0.0
    with:
      action: open
      url: "https://www.baidu.com"
  
  - name: 输入搜索关键词
    uses: ui/browser@1.0.0
    with:
      action: input
      by: id
      value: "kw"
      text: "RPA机器人流程自动化"
  
  - name: 点击搜索按钮
    uses: ui/browser@1.0.0
    with:
      action: click
      by: id
      value: "su"
  
  - name: 截图保存结果
    uses: ui/browser@1.0.0
    with:
      action: screenshot
      save_path: "./search_result.png"
```

---

## 🧠 AI增强使用示例
### 文本摘要
```yaml
steps:
  - name: 读取长文本
    uses: file/operation@1.0.0
    with:
      action: read
      file_path: "./长文档.txt"
    register: doc_content
  
  - name: AI摘要
    uses: ai/llm@1.0.0
    with:
      action: summarize
      provider: "openai"
      model: "gpt-3.5-turbo"
      input: "${{ steps.读取长文本.output.content }}"
```

### OCR识别图片文字
```yaml
steps:
  - name: 截图
    uses: ui/desktop@1.0.0
    with:
      action: screenshot
      save_path: "./screenshot.png"
  
  - name: OCR识别文字
    uses: ai/ocr@1.0.0
    with:
      action: recognize
      image_path: "./screenshot.png"
      lang: "ch"
    register: ocr_result
  
  - name: 输出识别结果
    uses: feishu/message@1.0.0
    with:
      receive_id: "ou_xxxxxx"
      content: "识别结果：\n${{ steps.OCR识别文字.output.full_text }}"
```
