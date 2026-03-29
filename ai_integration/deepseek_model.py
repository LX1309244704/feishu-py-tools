"""
DeepSeek模型集成
"""
import requests
from typing import List, Dict, Any
from ai_integration.base import AIModelBase


class DeepSeekModel(AIModelBase):
    """DeepSeek模型集成"""
    
    def __init__(self, api_key: str = None, model: str = "deepseek-chat"):
        """
        初始化DeepSeek模型
        
        Args:
            api_key: DeepSeek API密钥
            model: 模型名称
        """
        super().__init__(api_key, model)
        self.base_url = "https://api.deepseek.com/v1"
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        DeepSeek聊天接口
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            AI回复内容
        """
        if not self._validate_messages(messages):
            raise ValueError("消息格式无效")
        
        headers = self._get_headers()
        
        data = {
            "model": self.model,
            "messages": self._format_messages(messages),
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", 
                                headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            return result["choices"][0]["message"]["content"]
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            raise Exception(f"DeepSeek API错误: {error_msg}")
    
    def complete(self, prompt: str, 
                 temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        DeepSeek文本补全接口
        
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
        DeepSeek文本嵌入接口
        
        Args:
            text: 输入文本
            
        Returns:
            嵌入向量
        """
        headers = self._get_headers()
        
        data = {
            "model": "deepseek-embedding",
            "input": text
        }
        
        response = requests.post(f"{self.base_url}/embeddings", 
                                headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            return result["data"][0]["embedding"]
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            raise Exception(f"Embedding API错误: {error_msg}")
    
    def stream_chat(self, messages: List[Dict[str, str]], 
                    temperature: float = 0.7, max_tokens: int = 2000):
        """
        DeepSeek流式聊天接口（生成器）
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Yields:
            每次生成的文本片段
        """
        if not self._validate_messages(messages):
            raise ValueError("消息格式无效")
        
        headers = self._get_headers()
        
        data = {
            "model": self.model,
            "messages": self._format_messages(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", 
                                headers=headers, json=data, stream=True)
        
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
                        if data_obj.get("choices"):
                            delta = data_obj["choices"][0].get("delta", {})
                            if delta.get("content"):
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue
    
    def code_analysis(self, code: str, language: str = "Python") -> str:
        """
        代码分析
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            分析结果
        """
        prompt = f"""请分析以下{language}代码的性能、可读性和潜在问题：

```{language}
{code}
```

请从以下方面分析：
1. 代码复杂度
2. 性能优化建议
3. 安全性问题
4. 代码风格建议

分析结果："""
        
        return self.complete(prompt, temperature=0.5)
    
    def refactor(self, code: str, language: str = "Python") -> str:
        """
        代码重构
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            重构后的代码
        """
        prompt = f"""请重构以下{language}代码，提高可读性和性能：

```{language}
{code}
```

重构后的代码（请只输出代码，不要解释）："""
        
        return self.complete(prompt, temperature=0.3)
    
    def generate_tests(self, code: str, language: str = "Python") -> str:
        """
        生成单元测试
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            测试代码
        """
        prompt = f"""请为以下{language}代码生成单元测试（使用unittest框架）：

```{language}
{code}
```

测试代码："""
        
        return self.complete(prompt, temperature=0.3)
    
    def explain_code(self, code: str, language: str = "Python") -> str:
        """
        代码解释
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            代码解释
        """
        prompt = f"""请解释以下{language}代码的功能和实现原理：

```{language}
{code}
```

解释："""
        
        return self.complete(prompt, temperature=0.5)
