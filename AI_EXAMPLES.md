# 飞书Python工具箱 v1.2.0 - AI集成使用示例

## 🤖 AI模型使用

### 1. Claude模型使用

```python
from ai_integration.claude_model import ClaudeModel

# 初始化
claude = ClaudeModel(
    api_key="sk-ant-api03-xxxxx",
    model="claude-3-5-sonnet-20241022"
)

# 基本聊天
messages = [
    {"role": "user", "content": "你好！请介绍一下飞书Python工具箱"}
]
response = claude.chat(messages, temperature=0.7)
print(response)

# 文本补全
prompt = "飞书Python工具箱是一个"
completion = claude.complete(prompt)
print(completion)

# 情感分析
text = "这个产品太棒了！我非常喜欢！"
sentiment = claude.analyze_sentiment(text)
print(f"情感: {sentiment['sentiment']}")
print(f"分数: {sentiment['score']}")
print(f"关键词: {sentiment['keywords']}")

# 文本摘要
long_text = """
飞书Python工具箱是一个功能强大的飞书管理工具，
支持多维表格、文档、日历、任务、消息等多种功能。
它可以自动化日常办公，提高工作效率。
"""
summary = claude.summarize(long_text, max_length=50)
print(f"摘要: {summary}")

# 实体提取
news = "ABC科技的张三昨天在北京发布了新产品"
entities = claude.extract_entities(news)
print(f"实体: {entities}")

# 代码审查
code = """
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)
"""
review = claude.code_review(code, language="python")
print(f"代码审查：{review}")
```

---

### 2. GPT模型使用

```python
from ai_integration.gpt_model import GPTModel

# 初始化
gpt = GPTModel(
    api_key="sk-proj-xxxxx",
    model="gpt-4o"
)

# 基本聊天
messages = [
    {"role": "system", "content": "你是一个专业的数据分析助手"},
    {"role": "user", "content": "请分析这组数据：[1, 2, 3, 4, 5]"}
]
response = gpt.chat(messages, temperature=0.5)
print(response)

# 函数调用
functions = [{
    "name": "calculate_average",
    "description": "计算平均值",
    "parameters": {
        "type": "object",
        "properties": {
            "numbers": {
                "type": "array",
                "items": {"type": "number"},
                "description": "数字列表"
            }
        },
        "required": ["numbers"]
    }
}]

messages = [
    {"role": "user", "content": "计算1, 2, 3, 4, 5的平均值"}
]
result = gpt.function_call(messages, functions)
print(result)

# 图像生成
images = gpt.generate_image("一只可爱的猫", size="1024x1024", n=1)
print(f"图片URL: {images[0]}")

# 语音转文字（需要音频文件）
# transcript = gpt.transcribe("audio.mp3")
# print(transcript)

# 内容审核
text = "这是一条正常的内容"
moderation = gpt.moderate(text)
print(f"审核结果: {moderation}")

# 文本分类
categories = gpt.classify("这是一个关于AI的文章", ["技术", "娱乐", "体育"])
print(f"分类结果: {categories}")
```

---

### 3. DeepSeek模型使用

```python
from ai_integration.deepseek_model import DeepSeekModel

# 初始化
deepseek = DeepSeekModel(
    api_key="sk-xxxxx",
    model="deepseek-chat"
)

# 基本聊天
messages = [
    {"role": "user", "content": "什么是Python？"}
]
response = deepseek.chat(messages)
print(response)

# 代码分析
code = """
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x >= pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)
"""
analysis = deepseek.code_analysis(code, language="python")
print(f"代码分析：{analysis}")

# 代码重构
refactored = deepseek.refactor(code, language="python")
print(f"重构后：{refactored}")

# 生成单元测试
tests = deepseek.generate_tests(code, language="python")
print(f"测试代码：{tests}")

# 代码解释
explanation = deepseek.explain_code(code, language="python")
print(f"代码解释：{explanation}")
```

---

## 🧠 自然语言查询

### 基础查询

```python
from ai_integration.nl_query_processor import NLQueryProcessor
from ai_integration.claude_model import ClaudeModel
import pandas as pd

# 初始化
processor = NLQueryProcessor(ClaudeModel(api_key="sk-xxx"))

# 准备数据
data = [
    {"产品": "iPhone", "价格": 8000, "库存": 50},
    {"产品": "MacBook", "价格": 12000, "库存": 30},
    {"产品": "AirPods", "价格": 1500, "库存": 100}
]
df = pd.DataFrame(data)

# 查询1：统计数据
result = processor.process_query(
    "统计有多少种产品",
    context={"data": df}
)
print(result)

# 查询2：计算总额
result = processor.process_query(
    "计算库存总价值",
    context={"data": df}
)
print(result)

# 查询3：最大值
result = processor.process_query(
    "哪个产品库存最多",
    context={"data": df}
)
print(result)

# 查询4：排序
result = processor.process_query(
    "按价格从高到低排序",
    context={"data": df}
)
print(result)
```

---

### 高级查询

```python
# 带条件的查询
result = processor.process_query(
    "查询价格大于5000的产品",
    context={"data": df}
)
print(result)

# 生成SQL
sql = processor.convert_to_sql(
    "查询库存少于50的产品，按价格降序",
    table_name="products"
)
print(f"生成的SQL：{sql}")

# 解释查询
explanation = processor.explain_query(
    "统计总销售额",
    {"销售额": 50000, "订单数": 100}
)
print(f"解释：{explanation}")

# 推荐下一步操作
next_steps = processor.suggest_next_actions(
    "已分析完成销售数据",
    "目标是提高销售额"
)
print(f"建议下一步：{next_steps}")
```

---

## 💡 智能推荐

### 个性化推荐

```python
from ai_integration.recommendation_engine import RecommendationEngine
from ai_integration.claude_model import ClaudeModel

# 初始化
engine = RecommendationEngine(ClaudeModel(api_key="sk-xxx"))

# 添加用户历史
engine.add_user_history("user_001", {
    "type": "文档",
    "category": "技术文档",
    "timestamp": datetime.now()
})

# 生成推荐
recommendations = engine.recommend(
    user_id="user_001",
    context={"current_task": "数据分析"},
    n=5
)

print("推荐结果：")
for rec in recommendations:
    print(f"- {rec['title']} ({rec['category']})")
    print(f"  理由：{rec['reason']}")
    print(f"  分数：{rec['score']}")
```

---

### 内容推荐

```python
# 基于内容的推荐
recommendations = engine.recommend_based_on_content(
    "我想学习Python数据分析",
    n=5
)

print("学习资源推荐：")
for rec in recommendations:
    print(f"- {rec['title']} ({rec['type']})")
    print(f"  优先级：{rec['priority']}")
```

---

### 工具推荐

```python
# 工具推荐
tools = engine.suggest_tools(
    task="需要处理100MB的Excel文件",
    context={"file_format": "xlsx", "columns": 50}
)

print("推荐工具：")
for tool in tools:
    print(f"- {tool['tool']}")
    print(f"  用途：{tool['purpose']}")
    if 'command' in tool:
        print(f"  命令：{tool['command']}")
```

---

### 下一步操作推荐

```python
# 推荐下一步操作
steps = engine.recommend_next_steps(
    current_step="已完成飞书表格创建",
    goal="实现自动化工作流"
)

print("建议下一步操作：")
for i, step in enumerate(steps, 1):
    print(f"{i}. {step}")
```

---

## 🧹 数据清洗

### 自动化清洗

```python
from ai_integration.data_cleaner import DataCleaner
import pandas as pd

# 初始化
cleaner = DataCleaner()

# 准备脏数据
dirty_data = {
    "姓名": ["张三", "李四", " 王五", "  赵六  ", None],
    "年龄": [25, None, 30, 35, 28],
    "工资": [8000, 9000, None, 12000, 10000],
    "邮箱": ["zhangsan@example.com", "invalid-email", "wangwu@example.com", None, "zhaoliu@example.com"]
}
df = pd.DataFrame(dirty_data)

# 自动清洗
cleaned_df = cleaner.clean_dataframe(df)
print("清洗后数据：")
print(cleaned_df)
```

### 自定义清洗规则

```python
# 定义清洗规则
rules = [
    {
        "type": "handle_missing",
        "column": "年龄",
        "strategy": "median"
    },
    {
        "type": "handle_missing",
        "column": "工资",
        "strategy": "mean"
    },
    {
        "type": "validate_format",
        "column": "邮箱",
        "format": "email"
    },
    {
        "type": "standardize_text",
        "column": "姓名"
    },
    {
        "type": "remove_outliers",
        "column": "工资",
        "method": "iqr"
    }
]

# 应用规则
cleaned_df = cleaner.clean_dataframe(df, rules)
print("自定义规则清洗：")
print(cleaned_df)
```

### AI辅助清洗

```python
from ai_integration.claude_model import ClaudeModel

# 初始化AI清洗器
ai_cleaner = DataCleaner(ClaudeModel(api_key="sk-xxx"))

# AI辅助清洗
cleaned_df = ai_cleaner.ai_assisted_cleaned(
    df,
    description="员工信息数据，包含姓名、年龄、工资、邮箱"
)

print("AI辅助清洗：")
print(cleaned_df)
```

### 异常检测

```python
# 检测异常数据
analyzed_df = cleaner.detect_anomalies(
    df,
    column="工资",
    method="iqr"
)

# 查看异常记录
anomalies = analyzed_df[analyzed_df["工资_anomaly"] == True]
print(f"发现 {len(anomalies)} 条异常数据")
print(anomalies[["姓名", "工资", "工资_zscore"]])
```

### 清洗报告

```python
# 生成清洗报告
report = cleaner.generate_cleaning_report()
print(report)
```

---

## 🔄 完整示例：智能数据分析流程

```python
from ai_integration.nl_query_processor import NLQueryProcessor
from ai_integration.data_cleaner import DataCleaner
from ai_integration.recommendation_engine import RecommendationEngine
from ai_integration.claude_model import ClaudeModel
import pandas as pd

# 1. 初始化
claude = ClaudeModel(api_key="sk-xxx")
processor = NLQueryProcessor(claude)
cleaner = DataCleaner()
engine = RecommendationEngine(claude)

# 2. 读取和清洗数据
df = pd.read_csv("sales_data.csv")
cleaned_df = cleaner.clean_dataframe(df)

# 3. 自然语言分析
print("=== 数据分析 ===")
query = "分析本月销售额最高的3个产品类别"
result = processor.process_query(
    query,
    context={"data": cleaned_df}
)
print(f"分析结果：{result['result']}")

# 4. 智能建议
print("\n=== 智能建议 ===")
steps = engine.recommend_next_steps(
    current_step="已完成销售数据分析",
    goal="提高下月销售额"
)
for i, step in enumerate(steps, 1):
    print(f"{i}. {step}")

# 5. 生成清洗报告
print("\n=== 数据质量报告 ===")
report = cleaner.generate_cleaning_report()
print(report)
```

---

## 📚 更多资源

### 文档
- **README.md**：https://github.com/LX1309244704/weiyuan/blob/main/README.md
- **EXAMPLES.md**：https://github.com/LX1309244704/weiyuan/blob/main/EXAMPLES.md
- **CHANGELOG.md**：https://github.com/LX1309244704/weiyuan/blob/main/CHANGELOG.md
- **RELEASE_v1.2.0.md**：https://github.com/LX1309244704/weiyuan/blob/main/RELEASE_v1.2.0.md

### GitHub
- **仓库地址**：https://github.com/LX1309244704/weiyuan
- **发布页面**：https://github.com/LX1309244704/weiyuan/releases/tag/v1.2.0

---

**🦞 现在你可以用自然语言查询飞书数据，让AI帮你分析、推荐和优化！**

**v1.2.0版本核心亮点**：
- 🤖 支持3种AI模型
- 🧠 自然语言查询
- 💡 智能推荐
- 🧹 数据质量清洗
- 🔍 代码辅助开发

**立即体验AI增强的飞书管理！** 🚀
