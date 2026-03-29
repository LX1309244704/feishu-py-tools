"""
Claude AI模型集成
"""
import requests
from typing import List, Dict, Any
from ai_integration.base import AIModelBase


class ClaudeModel(AIModelBase):
    """Claude模型集成"""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        初始化Claude模型
        
        Args:
            api_key: Anthropic API密钥
            model: 模型名称
        """
        super().__init__(api_key, model)
        self.base_url = "https://api.anthropic.com/v1/messages"
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Claude聊天接口
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            AI回复内容
        """
        if not self._validate_messages(messages):
            raise ValueError("消息格式无效")
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # 格式化消息
        formatted_messages = self._format_messages(messages)
        
        # Claude API使用messages数组格式
        data = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": formatted_messages
        }
        
        response = requests.post(self.base_url, headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            return result.get("content", [{}])[0].get("text", "")
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            raise Exception(f"Claude API错误: {error_msg}")
    
    def complete(self, prompt: str, 
                 temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Claude文本补全接口
        
        Args:
            prompt: 提示词
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            补全内容
        """
        messages = [
            {"role": "user", "content": prompt}
        ]
        return self.chat(messages, temperature, max_tokens)
    
    def embed(self, text: str) -> List[float]:
        """
        Claude文本嵌入接口
        
        Args:
            text: 输入文本
            
        Returns:
            嵌入向量
        """
        # Claude目前不直接支持embedding API
        # 这里使用简单的词频统计作为fallback
        raise NotImplementedError("Claude暂不支持embedding API")
    
    def stream_chat(self, messages: List[Dict[str, str]], 
                    temperature: float = 0.7, max_tokens: int = 2000):
        """
        Claude流式聊天接口（生成器）
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Yields:
            每次生成的文本片段
        """
        if not self._validate_messages(messages):
            raise ValueError("消息格式无效")
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        formatted_messages = self._format_messages(messages)
        
        data = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": formatted_messages,
            "stream": True
        }
        
        response = requests.post(self.base_url, headers=headers, json=data, stream=True)
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    
                    try:
                        import json
                        data_obj = json.loads(data_str)
                        if data_obj.get("type") == "content_block_delta":
                            delta = data_obj.get("delta", {})
                            if delta.get("type") == "text_delta":
                                yield delta.get("text", "")
                    except json.JSONDecodeError:
                        continue
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        情感分析
        
        Args:
            text: 输入文本
            
        Returns:
            情感分析结果
        """
        prompt = f"""请分析以下文本的情感，并以JSON格式返回结果：
文本：{text}

请返回以下信息：
- sentiment: 情感类别（positive/negative/neutral）
- score: 情感分数（0-1）
- keywords: 关键词列表

返回格式：{{"sentiment": "...", "score": 0.8, "keywords": ["...", "..."]}}"""
        
        response = self.complete(prompt, temperature=0.3)
        
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "sentiment": "neutral",
                "score": 0.5,
                "keywords": []
            }
    
    def summarize(self, text: str, max_length: int = 200) -> str:
        """
        文本摘要
        
        Args:
            text: 输入文本
            max_length: 最大摘要长度
            
        Returns:
            摘要内容
        """
        prompt = f"""请对以下文本进行摘要，摘要长度不超过{max_length}字：

{text}

摘要："""
        
        return self.complete(prompt, temperature=0.5)
    
    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        实体提取
        
        Args:
            text: 输入文本
            
        Returns:
            实体列表
        """
        prompt = f"""请从以下文本中提取实体，并以JSON数组格式返回：
文本：{text}

请识别并提取以下类型的实体：
- 人名（person）
- 机构名（organization）
- 位置（location）
- 时间（date）
- 数量（quantity）

返回格式：[{{"text": "...", "type": "person"}}, ...]"""
        
        response = self.complete(prompt, temperature=0.3)
        
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            return []
    
    def translate(self, text: str, target_lang: str = "English") -> str:
        """
        翻译
        
        Args:
            text: 输入文本
            target_lang: 目标语言
            
        Returns:
            翻译结果
        """
        prompt = f"""请将以下文本翻译成{target_lang}：

{text}

翻译："""
        
        return self.complete(prompt, temperature=0.3)
    
    def code_review(self, code: str, language: str = "Python") -> str:
        """
        代码审查
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            审查意见
        """
        prompt = f"""请对以下{language}代码进行审查，指出潜在问题和改进建议：

```{language}
{code}
```

审查意见："""
        
        return self.complete(prompt, temperature=0.5)
