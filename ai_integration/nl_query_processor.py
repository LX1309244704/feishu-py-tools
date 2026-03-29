"""
自然语言查询处理器
"""
from typing import Dict, Any, List, Optional
import re
import json


class NLQueryProcessor:
    """自然语言查询处理器"""
    
    def __init__(self, ai_model):
        """
        初始化查询处理器
        
        Args:
            ai_model: AI模型实例
        """
        self.ai_model = ai_model
    
    def process_query(self, query: str, 
                     context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理自然语言查询
        
        Args:
            query: 自然语言查询
            context: 上下文信息
            
        Returns:
            查询结果
        """
        # 解析查询意图
        intent = self._detect_intent(query)
        
        # 提取查询参数
        params = self._extract_params(query, intent)
        
        # 执行查询
        result = self._execute_query(intent, params, context)
        
        return {
            "intent": intent,
            "params": params,
            "result": result,
            "query": query
        }
    
    def _detect_intent(self, query: str) -> str:
        """
        检测查询意图
        
        Args:
            query: 查询文本
            
        Returns:
            意图类型
        """
        query_lower = query.lower()
        
        # 查询意图映射
        intent_patterns = {
            "search": ["查询", "搜索", "找", "查看", "获取"],
            "count": ["统计", "数量", "多少", "几个", "计数"],
            "sum": ["总计", "总和", "求和", "总金额"],
            "avg": ["平均", "均值", "平均值"],
            "max": ["最大", "最高", "最多", "排行"],
            "min": ["最小", "最低", "最少"],
            "filter": ["筛选", "过滤", "符合条件的"],
            "recent": ["最近", "近期", "最新", "本周", "本月"],
            "sort": ["排序", "排列", "按...排序"],
            "analyze": ["分析", "评估", "判断", "对比"],
            "predict": ["预测", "预计", "估算", "将来"],
            "recommend": ["推荐", "建议", "应该", "最佳"]
        }
        
        # 匹配意图
        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if pattern in query_lower:
                    return intent
        
        # 默认意图
        return "search"
    
    def _extract_params(self, query: str, intent: str) -> Dict[str, Any]:
        """
        提取查询参数
        
        Args:
            query: 查询文本
            intent: 查询意图
            
        Returns:
            参数字典
        """
        params = {}
        
        # 提取数字
        numbers = re.findall(r'\d+', query)
        if numbers:
            params["numbers"] = [int(n) for n in numbers]
        
        # 提取时间范围
        time_patterns = {
            "today": ["今天", "今日"],
            "yesterday": ["昨天", "昨日"],
            "this_week": ["本周", "这周"],
            "last_week": ["上周", "这周"],
            "this_month": ["本月", "这个月"],
            "last_month": ["上月", "上个月"],
            "this_year": ["今年", "本年"],
            "last_year": ["去年", "上一年"]
        }
        
        for time_key, patterns in time_patterns.items():
            for pattern in patterns:
                if pattern in query:
                    params["time_range"] = time_key
                    break
        
        # 提取条件
        condition_pattern = r'([^\s]+)\s*[=><!]+\s*([^\s]+)'
        conditions = re.findall(condition_pattern, query)
        if conditions:
            params["conditions"] = [
                {"field": cond[0], "operator": "eq", "value": cond[1]}
                for cond in conditions
            ]
        
        # 提取排序字段
        sort_pattern = r'按\s*([^\s]+)\s*(升序|降序|asc|desc|正序|倒序)'
        sort_match = re.search(sort_pattern, query)
        if sort_match:
            params["sort_field"] = sort_match.group(1)
            params["sort_order"] = sort_match.group(2)
        
        # 提取限制数量
        limit_pattern = r'(前|前|top|只显示)\s*(\d+)\s*(个|条|条|项)'
        limit_match = re.search(limit_pattern, query)
        if limit_match:
            params["limit"] = int(limit_match.group(2))
        
        return params
    
    def _execute_query(self, intent: str, params: Dict[str, Any],
                      context: Dict[str, Any] = None) -> Any:
        """
        执行查询
        
        Args:
            intent: 查询意图
            params: 查询参数
            context: 上下文信息
            
        Returns:
            查询结果
        """
        # 如果有数据上下文，使用AI处理
        if context and "data" in context:
            return self._execute_with_data(intent, params, context["data"])
        
        # 没有数据上下文，生成查询建议
        return self._generate_query_suggestion(intent, params)
    
    def _execute_with_data(self, intent: str, params: Dict[str, Any], 
                           data: List[Dict[str, Any]]) -> Any:
        """
        在数据上执行查询
        
        Args:
            intent: 查询意图
            params: 查询参数
            data: 数据列表
            
        Returns:
            查询结果
        """
        import pandas as pd
        
        df = pd.DataFrame(data)
        
        # 应用筛选条件
        if "conditions" in params:
            for condition in params["conditions"]:
                field = condition["field"]
                value = condition["value"]
                if field in df.columns:
                    df = df[df[field] == value]
        
        # 应用时间范围
        if "time_range" in params and "时间" in df.columns:
            # 这里需要根据实际的时间字段和格式处理
            pass
        
        # 应用限制
        if "limit" in params:
            df = df.head(params["limit"])
        
        # 执行聚合操作
        if intent == "count":
            return len(df)
        
        elif intent == "sum":
            numeric_cols = df.select_dtypes(include=['number']).columns
            if not numeric_cols.empty:
                return df[numeric_cols].sum().to_dict()
            return "没有数值字段可求和"
        
        elif intent == "avg":
            numeric_cols = df.select_dtypes(include=['number']).columns
            if not numeric_cols.empty:
                return df[numeric_cols].mean().to_dict()
            return "没有数值字段可求平均"
        
        elif intent == "max":
            numeric_cols = df.select_dtypes(include=['number']).columns
            if not numeric_cols.empty:
                return df[numeric_cols].max().to_dict()
            return "没有数值字段可求最大值"
        
        elif intent == "min":
            numeric_cols = df.select_dtypes(include=['number']).columns
            if not numeric_cols.empty:
                return df[numeric_cols].min().to_dict()
            return "没有数值字段可求最小值"
        
        elif intent == "search":
            return df.to_dict('records')
        
        elif intent == "sort":
            sort_field = params.get("sort_field")
            if sort_field and sort_field in df.columns:
                ascending = params.get("sort_order", "asc") in ["升序", "asc", "正序"]
                return df.sort_values(by=sort_field, ascending=ascending).to_dict('records')
            return df.to_dict('records')
        
        else:
            return df.to_dict('records')
    
    def _generate_query_suggestion(self, intent: str, 
                                   params: Dict[str, Any]) -> str:
        """
        生成查询建议
        
        Args:
            intent: 查询意图
            params: 查询参数
            
        Returns:
            查询建议
        """
        suggestions = {
            "search": "我可以帮你搜索数据，请提供表名和筛选条件",
            "count": "我可以帮你统计数据数量，请告诉我统计哪个表",
            "sum": "我可以帮你计算总和，请告诉我哪个数值字段",
            "avg": "我可以帮你计算平均值，请告诉我哪个数值字段",
            "max": "我可以帮你找出最大值，请告诉我哪个字段",
            "min": "我可以帮你找出最小值，请告诉我哪个字段",
            "filter": "我可以帮你筛选数据，请提供筛选条件",
            "recent": "我可以帮你查询最近的数据，请提供表名",
            "sort": "我可以帮你排序数据，请告诉我排序字段",
            "analyze": "我可以帮你分析数据，请提供数据集",
            "predict": "我可以帮你预测趋势，请提供历史数据",
            "recommend": "我可以给你提供建议，请告诉我你的需求"
        }
        
        return suggestions.get(intent, "请提供更详细的查询信息")
    
    def explain_query(self, query: str, result: Any) -> str:
        """
        解释查询结果
        
        Args:
            query: 原始查询
            result: 查询结果
            
        Returns:
            解释文本
        """
        prompt = f"""请用自然语言解释以下查询和结果：

查询：{query}

结果：{result}

请用简洁易懂的语言解释查询的含义和结果。"""
        
        return self.ai_model.complete(prompt)
    
    def convert_to_sql(self, query: str, table_name: str = "data") -> str:
        """
        将自然语言查询转换为SQL
        
        Args:
            query: 自然语言查询
            table_name: 表名
            
        Returns:
            SQL语句
        """
        intent = self._detect_intent(query)
        params = self._extract_params(query, intent)
        
        sql = f"SELECT * FROM {table_name}"
        
        # 添加WHERE条件
        where_clauses = []
        if "conditions" in params:
            for cond in params["conditions"]:
                where_clauses.append(f"{cond['field']} = '{cond['value']}'")
        
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        
        # 添加ORDER BY
        if "sort_field" in params:
            sort_order = params.get("sort_order", "asc")
            if sort_order in ["降序", "desc", "倒序"]:
                sql += f" ORDER BY {params['sort_field']} DESC"
            else:
                sql += f" ORDER BY {params['sort_field']} ASC"
        
        # 添加LIMIT
        if "limit" in params:
            sql += f" LIMIT {params['limit']}"
        
        return sql
    
    def suggest_next_actions(self, query: str, result: Any) -> List[str]:
        """
        建议后续操作
        
        Args:
            query: 原始查询
            result: 查询结果
            
        Returns:
            建议操作列表
        """
        prompt = f"""根据以下查询和结果，建议3-5个有用的后续操作：

查询：{query}
结果：{result}

请返回JSON格式的建议列表：
[["操作1", "说明"], ["操作2", "说明"], ...]"""
        
        response = self.ai_model.complete(prompt)
        
        try:
            suggestions = json.loads(response)
            return [suggestion[0] for suggestion in suggestions]
        except json.JSONDecodeError:
            return [
                "导出结果",
                "筛选更多信息",
                "进行数据可视化"
            ]
