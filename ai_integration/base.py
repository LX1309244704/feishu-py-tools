"""
AI模型基础类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class AIModelBase(ABC):
    """AI模型基础类"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        初始化AI模型
        
        Args:
            api_key: API密钥
            model: 模型名称
        """
        self.api_key = api_key
        self.model = model
        self.base_url = None
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        聊天接口
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            AI回复内容
        """
        pass
    
    @abstractmethod
    def complete(self, prompt: str, 
                 temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        文本补全接口
        
        Args:
            prompt: 提示词
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            补全内容
        """
        pass
    
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """
        文本嵌入接口
        
        Args:
            text: 输入文本
            
        Returns:
            嵌入向量
        """
        pass
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        格式化消息
        
        Args:
            messages: 原始消息列表
            
        Returns:
            格式化后的消息列表
        """
        formatted = []
        for msg in messages:
            if msg.get("role") == "system":
                formatted.append({"role": "system", "content": msg.get("content")})
            elif msg.get("role") == "user":
                formatted.append({"role": "user", "content": msg.get("content")})
            elif msg.get("role") == "assistant":
                formatted.append({"role": "assistant", "content": msg.get("content")})
        
        return formatted
    
    def _validate_messages(self, messages: List[Dict[str, str]]) -> bool:
        """
        验证消息格式
        
        Args:
            messages: 消息列表
            
        Returns:
            是否有效
        """
        if not messages:
            return False
        
        for msg in messages:
            if not isinstance(msg, dict):
                return False
            if "role" not in msg or "content" not in msg:
                return False
            if msg["role"] not in ["system", "user", "assistant"]:
                return False
        
        return True
    
    def estimate_tokens(self, text: str) -> int:
        """
        估算token数量
        
        Args:
            text: 输入文本
            
        Returns:
            token数量估算
        """
        # 简单估算：中文字符*1.5 + 英文字符*0.25
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english_chars = len(text) - chinese_chars
        
        return int(chinese_chars * 1.5 + english_chars * 0.25)
