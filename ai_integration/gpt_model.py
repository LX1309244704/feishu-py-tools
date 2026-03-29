"""
OpenAI GPT模型集成
"""
import requests
from typing import List, Dict, Any
from ai_integration.base import AIModelBase


class GPTModel(AIModelBase):
    """OpenAI GPT模型集成"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        """
        初始化GPT模型
        
        Args:
            api_key: OpenAI API密钥
            model: 模型名称
        """
        super().__init__(api_key, model)
        self.base_url = "https://api.openai.com/v1"
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        GPT聊天接口
        
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
            raise Exception(f"GPT API错误: {error_msg}")
    
    def complete(self, prompt: str, 
                 temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        GPT文本补全接口
        
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
        GPT文本嵌入接口
        
        Args:
            text: 输入文本
            
        Returns:
            嵌入向量
        """
        headers = self._get_headers()
        
        data = {
            "model": "text-embedding-3-small",
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
        GPT流式聊天接口（生成器）
        
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
    
    def function_call(self, messages: List[Dict[str, str]], 
                     functions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        函数调用接口
        
        Args:
            messages: 消息列表
            functions: 函数定义列表
            
        Returns:
            函数调用结果
        """
        if not self._validate_messages(messages):
            raise ValueError("消息格式无效")
        
        headers = self._get_headers()
        
        data = {
            "model": self.model,
            "messages": self._format_messages(messages),
            "functions": functions,
            "function_call": "auto"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", 
                                headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            choice = result["choices"][0]
            if "function_call" in choice["message"]:
                return choice["message"]["function_call"]
            else:
                return {"content": choice["message"]["content"]}
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            raise Exception(f"Function Call API错误: {error_msg}")
    
    def generate_image(self, prompt: str, size: str = "1024x1024", 
                      n: int = 1) -> List[str]:
        """
        图像生成接口
        
        Args:
            prompt: 图像描述
            size: 图像尺寸
            n: 生成数量
            
        Returns:
            图像URL列表
        """
        headers = self._get_headers()
        
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": size,
            "n": n
        }
        
        response = requests.post(f"{self.base_url}/images/generations", 
                                headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            return [img["url"] for img in result["data"]]
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            raise Exception(f"Image Generation API错误: {error_msg}")
    
    def transcribe(self, audio_file: str, language: str = "zh") -> str:
        """
        语音转文字
        
        Args:
            audio_file: 音频文件路径
            language: 语言代码
            
        Returns:
            转录文本
        """
        headers = self._get_headers()
        
        with open(audio_file, "rb") as f:
            files = {
                "file": ("audio.mp3", f, "audio/mpeg")
            }
            data = {
                "model": "whisper-1",
                "language": language
            }
            
            response = requests.post(f"{self.base_url}/audio/transcriptions", 
                                    headers=headers, data=data, files=files)
            result = response.json()
            
            if response.status_code == 200:
                return result["text"]
            else:
                error_msg = result.get("error", {}).get("message", "Unknown error")
                raise Exception(f"Transcription API错误: {error_msg}")
    
    def moderate(self, text: str) -> Dict[str, Any]:
        """
        内容审核
        
        Args:
            text: 待审核文本
            
        Returns:
            审核结果
        """
        headers = self._get_headers()
        
        data = {
            "input": text
        }
        
        response = requests.post(f"{self.base_url}/moderations", 
                                headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            return result["results"][0]
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            raise Exception(f"Moderation API错误: {error_msg}")
    
    def classify(self, text: str, categories: List[str]) -> Dict[str, float]:
        """
        文本分类
        
        Args:
            text: 输入文本
            categories: 类别列表
            
        Returns:
            分类结果
        """
        categories_str = "、".join(categories)
        prompt = f"""请将以下文本分类到以下类别之一：{categories_str}

文本：{text}

请返回JSON格式：{{"category": "...", "confidence": 0.9}}"""
        
        response = self.complete(prompt, temperature=0.3)
        
        try:
            import json
            result = json.loads(response)
            # 将字符串转换为字典格式
            if isinstance(result, dict):
                return {result.get("category", ""): result.get("confidence", 0.0)}
            return {}
        except json.JSONDecodeError:
            return {}
