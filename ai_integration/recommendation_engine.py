"""
智能推荐引擎
"""
from typing import Dict, Any, List, Optional
import numpy as np
from collections import defaultdict


class RecommendationEngine:
    """智能推荐引擎"""
    
    def __init__(self, ai_model):
        """
        初始化推荐引擎
        
        Args:
            ai_model: AI模型实例
        """
        self.ai_model = ai_model
        self.user_history = defaultdict(list)
        self.item_features = {}
    
    def recommend(self, user_id: str, context: Dict[str, Any] = None,
                n: int = 5) -> List[Dict[str, Any]]:
        """
        为用户生成推荐
        
        Args:
            user_id: 用户ID
            context: 上下文信息
            n: 推荐数量
            
        Returns:
            推荐结果列表
        """
        # 获取用户历史
        history = self.user_history.get(user_id, [])
        
        # 分析用户偏好
        user_preferences = self._analyze_preferences(history)
        
        # 生成推荐
        recommendations = self._generate_recommendations(
            user_preferences, context, n
        )
        
        return recommendations
    
    def _analyze_preferences(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析用户偏好
        
        Args:
            history: 用户历史记录
            
        Returns:
            用户偏好字典
        """
        preferences = {
            "categories": defaultdict(int),
            "features": defaultdict(int),
            "time_patterns": defaultdict(int)
        }
        
        for item in history:
            # 分析类别偏好
            if "category" in item:
                preferences["categories"][item["category"]] += 1
            
            # 分析特征偏好
            if "features" in item:
                for feature in item["features"]:
                    preferences["features"][feature] += 1
            
            # 分析时间偏好
            if "timestamp" in item:
                hour = item["timestamp"].hour
                preferences["time_patterns"][f"hour_{hour}"] += 1
        
        return preferences
    
    def _generate_recommendations(self, preferences: Dict[str, Any],
                                 context: Dict[str, Any], n: int) -> List[Dict[str, Any]]:
        """
        生成推荐
        
        Args:
            preferences: 用户偏好
            context: 上下文信息
            n: 推荐数量
            
        Returns:
            推荐列表
        """
        # 如果有AI模型，使用AI生成推荐
        if self.ai_model:
            return self._ai_generate_recommendations(preferences, context, n)
        
        # 否则使用规则推荐
        return self._rule_generate_recommendations(preferences, context, n)
    
    def _ai_generate_recommendations(self, preferences: Dict[str, Any],
                                     context: Dict[str, Any], n: int) -> List[Dict[str, Any]]:
        """
        使用AI生成推荐
        
        Args:
            preferences: 用户偏好
            context: 上下文信息
            n: 推荐数量
            
        Returns:
            推荐列表
        """
        prompt = f"""根据以下用户偏好，生成{n}个推荐：

用户偏好：
- 喜欢的类别：{list(preferences['categories'].keys())}
- 喜欢的特征：{list(preferences['features'].keys())}
- 活跃时间段：{list(preferences['time_patterns'].keys())}

当前上下文：{context}

请返回JSON格式的推荐列表：
[
  {{"id": "1", "title": "推荐1", "category": "类别", "reason": "推荐理由", "score": 0.9}},
  {{"id": "2", "title": "推荐2", "category": "类别", "reason": "推荐理由", "score": 0.8}},
  ...
]"""
        
        response = self.ai_model.complete(prompt, temperature=0.7)
        
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            return []
    
    def _rule_generate_recommendations(self, preferences: Dict[str, Any],
                                      context: Dict[str, Any], n: int) -> List[Dict[str, Any]]:
        """
        使用规则生成推荐
        
        Args:
            preferences: 用户偏好
            context: 上下文信息
            n: 推荐数量
            
        Returns:
            推荐列表
        """
        recommendations = []
        
        # 基于类别偏好的推荐
        top_categories = sorted(preferences["categories"].items(), 
                              key=lambda x: x[1], reverse=True)[:3]
        
        for category, count in top_categories:
            if len(recommendations) >= n:
                break
            
            recommendations.append({
                "id": f"rec_{len(recommendations)}",
                "title": f"{category}相关推荐",
                "category": category,
                "reason": f"您对{category}类别的内容表现出兴趣",
                "score": min(0.9, count / max(preferences["categories"].values()))
            })
        
        return recommendations[:n]
    
    def add_user_history(self, user_id: str, item: Dict[str, Any]):
        """
        添加用户历史记录
        
        Args:
            user_id: 用户ID
            item: 历史记录项
        """
        self.user_history[user_id].append(item)
    
    def update_item_features(self, item_id: str, features: Dict[str, Any]):
        """
        更新项目特征
        
        Args:
            item_id: 项目ID
            features: 特征字典
        """
        self.item_features[item_id] = features
    
    def find_similar_items(self, item_id: str, n: int = 5) -> List[Dict[str, Any]]:
        """
        找到相似的项目
        
        Args:
            item_id: 项目ID
            n: 返回数量
            
        Returns:
            相似项目列表
        """
        if item_id not in self.item_features:
            return []
        
        target_features = self.item_features[item_id]
        similarities = []
        
        for other_id, other_features in self.item_features.items():
            if other_id == item_id:
                continue
            
            similarity = self._calculate_similarity(target_features, other_features)
            similarities.append({
                "id": other_id,
                "similarity": similarity
            })
        
        # 按相似度排序
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similarities[:n]
    
    def _calculate_similarity(self, features1: Dict[str, Any], 
                             features2: Dict[str, Any]) -> float:
        """
        计算特征相似度
        
        Args:
            features1: 特征1
            features2: 特征2
            
        Returns:
            相似度分数（0-1）
        """
        # 简单的Jaccard相似度
        keys1 = set(features1.keys())
        keys2 = set(features2.keys())
        
        intersection = keys1 & keys2
        union = keys1 | keys2
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def recommend_based_on_content(self, content: str, 
                                  n: int = 5) -> List[Dict[str, Any]]:
        """
        基于内容的推荐
        
        Args:
            content: 内容文本
            n: 推荐数量
            
        Returns:
            推荐列表
        """
        # 使用AI分析内容，生成推荐
        prompt = f"""根据以下内容，推荐{n}个相关的操作或资源：

内容：{content}

请返回JSON格式的推荐列表：
[
  {{"title": "推荐1", "type": "操作/资源", "reason": "推荐理由", "priority": "high/medium/low"}},
  {{"title": "推荐2", "type": "操作/资源", "reason": "推荐理由", "priority": "high/medium/low"}},
  ...
]"""
        
        response = self.ai_model.complete(prompt, temperature=0.7)
        
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            return []
    
    def recommend_next_steps(self, current_step: str, 
                           goal: str = None) -> List[str]:
        """
        推荐下一步操作
        
        Args:
            current_step: 当前步骤
            goal: 目标（可选）
            
        Returns:
            推荐的下一步操作列表
        """
        prompt = f"""当前步骤：{current_step}
目标：{goal if goal else '未指定'}

请推荐3-5个合理的下一步操作，按优先级排序。

请直接返回操作列表，不要解释。"""
        
        response = self.ai_model.complete(prompt, temperature=0.5)
        
        # 解析响应，提取操作列表
        steps = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # 移除序号和符号
                clean_line = re.sub(r'^[\d\.\-\*]+\s*', '', line)
                if clean_line:
                    steps.append(clean_line)
        
        return steps[:5] if steps else ["继续当前操作", "检查进度", "更新计划"]
    
    def personalize_response(self, user_id: str, 
                            message: str) -> str:
        """
        个性化回复
        
        Args:
            user_id: 用户ID
            message: 原始消息
            
        Returns:
            个性化后的回复
        """
        history = self.user_history.get(user_id, [])
        
        if not history:
            return message
        
        # 分析用户习惯
        preferences = self._analyze_preferences(history)
        
        # 根据偏好调整回复风格
        if preferences["features"].get("formal", 0) > preferences["features"].get("casual", 0):
            # 用户偏好正式风格
            if not message.endswith('。') and not message.endswith('！'):
                message += '。'
        else:
            # 用户偏好随意风格
            pass
        
        return message
    
    def suggest_tools(self, task: str, context: Dict[str, Any] = None) -> List[str]:
        """
        根据任务推荐工具
        
        Args:
            task: 任务描述
            context: 上下文信息
            
        Returns:
            推荐的工具列表
        """
        prompt = f"""任务：{task}
上下文：{context}

请推荐3-5个适合的工具来完成任务，并说明每个工具的用途。

请返回JSON格式：
[
  {{"tool": "工具1", "purpose": "用途", "command": "命令示例"}},
  {{"tool": "工具2", "purpose": "用途", "command": "命令示例"}},
  ...
]"""
        
        response = self.ai_model.complete(prompt, temperature=0.7)
        
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            return []
