"""
数据清洗器
"""
from typing import List, Dict, Any, Optional, Callable
import re
import pandas as pd
import numpy as np
from datetime import datetime
import hashlib


class DataCleaner:
    """数据清洗器"""
    
    def __init__(self, ai_model=None):
        """
        初始化数据清洗器
        
        Args:
            ai_model: AI模型实例（可选）
        """
        self.ai_model = ai_model
        self.cleaning_rules = {}
        self.cleaning_stats = {}
    
    def clean_dataframe(self, df: pd.DataFrame, 
                      rules: List[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        清洗DataFrame
        
        Args:
            df: 原始DataFrame
            rules: 清洗规则列表
            
        Returns:
            清洗后的DataFrame
        """
        # 记录原始数据统计
        self.cleaning_stats["original"] = {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": df.isnull().sum().sum(),
            "duplicates": df.duplicated().sum()
        }
        
        cleaned_df = df.copy()
        
        # 应用清洗规则
        if rules:
            for rule in rules:
                cleaned_df = self._apply_rule(cleaned_df, rule)
        else:
            # 应用默认清洗规则
            cleaned_df = self._apply_default_rules(cleaned_df)
        
        # 记录清洗后统计
        self.cleaning_stats["cleaned"] = {
            "rows": len(cleaned_df),
            "columns": len(cleaned_df.columns),
            "missing_values": cleaned_df.isnull().sum().sum(),
            "duplicates": cleaned_df.duplicated().sum()
        }
        
        return cleaned_df
    
    def _apply_default_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        应用默认清洗规则
        
        Args:
            df: 原始DataFrame
            
        Returns:
            清洗后的DataFrame
        """
        # 1. 删除完全为空的行
        df = df.dropna(how='all')
        
        # 2. 删除完全为空的列
        df = df.dropna(axis=1, how='all')
        
        # 3. 删除重复行
        df = df.drop_duplicates()
        
        # 4. 处理缺失值
        for col in df.columns:
            if df[col].dtype in ['object', 'string']:
                # 字符串类型：填充"未知"
                df[col] = df[col].fillna("未知")
            elif df[col].dtype in ['int64', 'float64']:
                # 数值类型：填充0
                df[col] = df[col].fillna(0)
            elif df[col].dtype == 'datetime64[ns]':
                # 日期类型：填充当前时间
                df[col] = df[col].fillna(datetime.now())
        
        # 5. 去除字符串两端的空白
        str_cols = df.select_dtypes(include=['object', 'string']).columns
        for col in str_cols:
            df[col] = df[col].str.strip()
        
        # 6. 标准化文本（小写）
        for col in str_cols:
            if col.lower() in ['name', 'title', 'email', 'phone']:
                df[col] = df[col].str.lower()
        
        return df
    
    def _apply_rule(self, df: pd.DataFrame, rule: Dict[str, Any]) -> pd.DataFrame:
        """
        应用单个清洗规则
        
        Args:
            df: DataFrame
            rule: 清洗规则
            
        Returns:
            处理后的DataFrame
        """
        rule_type = rule.get("type")
        column = rule.get("column")
        
        if rule_type == "remove_duplicates":
            if column:
                df = df.drop_duplicates(subset=[column])
            else:
                df = df.drop_duplicates()
        
        elif rule_type == "handle_missing":
            strategy = rule.get("strategy", "mean")
            if column in df.columns:
                if strategy == "mean":
                    if df[column].dtype in ['int64', 'float64']:
                        df[column] = df[column].fillna(df[column].mean())
                elif strategy == "median":
                    if df[column].dtype in ['int64', 'float64']:
                        df[column] = df[column].fillna(df[column].median())
                elif strategy == "mode":
                    df[column] = df[column].fillna(df[column].mode()[0])
                elif strategy == "drop":
                    df = df.dropna(subset=[column])
                elif strategy == "fill":
                    df[column] = df[column].fillna(rule.get("value", ""))
        
        elif rule_type == "standardize_text":
            if column and column in df.columns:
                df[column] = self._standardize_text(df[column])
        
        elif rule_type == "remove_outliers":
            if column and column in df.columns:
                df = self._remove_outliers(df, column, rule.get("method", "iqr"))
        
        elif rule_type == "validate_format":
            if column and column in df.columns:
                df = self._validate_format(df, column, rule.get("format", None))
        
        elif rule_type == "normalize_values":
            if column and column in df.columns:
                df[column] = self._normalize_values(df, column)
        
        return df
    
    def _standardize_text(self, series: pd.Series) -> pd.Series:
        """
        标准化文本
        
        Args:
            series: 文本系列
            
        Returns:
            标准化后的系列
        """
        # 移除前后空格
        series = series.str.strip()
        
        # 转换为小写
        series = series.str.lower()
        
        # 移除特殊字符
        series = series.str.replace(r'[^\w\s]', '', regex=True)
        
        # 移除多余空格
        series = series.str.replace(r'\s+', ' ', regex=True)
        
        return series
    
    def _remove_outliers(self, df: pd.DataFrame, column: str, 
                         method: str = "iqr") -> pd.DataFrame:
        """
        移除异常值
        
        Args:
            df: DataFrame
            column: 列名
            method: 方法（iqr/zscore）
            
        Returns:
            处理后的DataFrame
        """
        if column not in df.columns or df[column].dtype not in ['int64', 'float64']:
            return df
        
        if method == "iqr":
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        
        elif method == "zscore":
            mean = df[column].mean()
            std = df[column].std()
            z_scores = np.abs((df[column] - mean) / std)
            return df[z_scores < 3]
        
        return df
    
    def _validate_format(self, df: pd.DataFrame, column: str,
                        format_type: str) -> pd.DataFrame:
        """
        验证格式
        
        Args:
            df: DataFrame
            column: 列名
            format_type: 格式类型
            
        Returns:
            处理后的DataFrame
        """
        if column not in df.columns:
            return df
        
        if format_type == "email":
            # 验证邮箱格式
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            valid_mask = df[column].str.match(pattern, na=False)
            invalid_rows = df[~valid_mask]
            
            if len(invalid_rows) > 0:
                print(f"发现 {len(invalid_rows)} 行无效的邮箱格式，已标记")
                df[f"{column}_valid"] = valid_mask
        
        elif format_type == "phone":
            # 验证手机号格式
            pattern = r'^1[3-9]\d{9}$'
            valid_mask = df[column].astype(str).str.match(pattern, na=False)
            invalid_rows = df[~valid_mask]
            
            if len(invalid_rows) > 0:
                print(f"发现 {len(invalid_rows)} 行无效的手机号格式，已标记")
                df[f"{column}_valid"] = valid_mask
        
        elif format_type == "date":
            # 验证日期格式
            try:
                df[column] = pd.to_datetime(df[column], errors='coerce')
            except:
                pass
        
        return df
    
    def _normalize_values(self, df: pd.DataFrame, column: str) -> pd.Series:
        """
        标准化数值
        
        Args:
            df: DataFrame
            column: 列名
            
        Returns:
            标准化后的系列
        """
        if column not in df.columns or df[column].dtype not in ['int64', 'float64']:
            return df[column]
        
        mean = df[column].mean()
        std = df[column].std()
        
        if std == 0:
            return df[column]
        
        return (df[column] - mean) / std
    
    def deduplicate_by_fingerprint(self, df: pd.DataFrame, 
                                  columns: List[str] = None) -> pd.DataFrame:
        """
        基于指纹去重
        
        Args:
            df: DataFrame
            columns: 用于生成指纹的列
            
        Returns:
            去重后的DataFrame
        """
        if columns is None:
            columns = df.select_dtypes(include=['object', 'string']).columns.tolist()
        
        # 生成指纹
        def generate_fingerprint(row):
            combined = ''.join(str(row[col]) for col in columns)
            return hashlib.md5(combined.encode()).hexdigest()
        
        fingerprints = df.apply(generate_fingerprint, axis=1)
        
        # 检查重复指纹
        df['_fingerprint'] = fingerprints
        duplicate_mask = fingerprints.duplicated(keep='first')
        
        print(f"发现 {duplicate_mask.sum()} 条重复记录")
        
        return df[~duplicate_mask].drop(columns=['_fingerprint'])
    
    def detect_anomalies(self, df: pd.DataFrame, column: str,
                          method: str = "isolation_forest") -> pd.DataFrame:
        """
        检测异常数据
        
        Args:
            df: DataFrame
            column: 列名
            method: 检测方法
            
        Returns:
            包含异常标记的DataFrame
        """
        if column not in df.columns or df[column].dtype not in ['int64', 'float64']:
            return df
        
        # 简单的Z-score方法
        if method == "zscore":
            mean = df[column].mean()
            std = df[column].std()
            z_scores = np.abs((df[column] - mean) / std)
            df[f"{column}_anomaly"] = z_scores > 3
            df[f"{column}_zscore"] = z_scores
        
        # IQR方法
        elif method == "iqr":
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            df[f"{column}_anomaly"] = (df[column] < lower_bound) | (df[column] > upper_bound)
        
        return df
    
    def generate_cleaning_report(self) -> str:
        """
        生成清洗报告
        
        Returns:
            清洗报告文本
        """
        original = self.cleaning_stats.get("original", {})
        cleaned = self.cleaning_stats.get("cleaned", {})
        
        report = f"""
=== 数据清洗报告 ===

原始数据：
- 行数：{original.get('rows', 0)}
- 列数：{original.get('columns', 0)}
- 缺失值：{original.get('missing_values', 0)}
- 重复行：{original.get('duplicates', 0)}

清洗后数据：
- 行数：{cleaned.get('rows', 0)}
- 列数：{cleaned.get('columns', 0)}
- 缺失值：{cleaned.get('missing_values', 0)}
- 重复行：{cleaned.get('duplicates', 0)}

变化统计：
- 删除行数：{original.get('rows', 0) - cleaned.get('rows', 0)}
- 删除列数：{original.get('columns', 0) - cleaned.get('columns', 0)}
- 处理缺失值：{original.get('missing_values', 0) - cleaned.get('missing_values', 0)}
- 删除重复：{original.get('duplicates', 0) - cleaned.get('duplicates', 0)}
"""
        
        return report.strip()
    
    def ai_assisted_cleaning(self, df: pd.DataFrame, 
                            description: str = "") -> pd.DataFrame:
        """
        AI辅助清洗
        
        Args:
            df: 原始DataFrame
            description: 数据描述
            
        Returns:
            清洗后的DataFrame
        """
        if not self.ai_model:
            print("AI模型未配置，使用默认清洗规则")
            return self._apply_default_rules(df)
        
        prompt = f"""数据描述：{description}

数据预览：
{df.head()}

请分析数据质量问题并建议清洗策略。返回JSON格式：
{{
  "issues": [
    {{"type": "missing_values", "columns": ["col1", "col2"], "strategy": "mean"}},
    {{"type": "outliers", "columns": ["col3"], "strategy": "iqr"}},
    {{"type": "duplicates", "strategy": "keep_first"}}
  ],
  "recommendations": [
    "建议1",
    "建议2"
  ]
}}"""
        
        response = self.ai_model.complete(prompt)
        
        try:
            import json
            analysis = json.loads(response)
            
            # 应用AI建议的清洗策略
            for issue in analysis.get("issues", []):
                if issue["type"] == "missing_values":
                    for col in issue["columns"]:
                        if col in df.columns:
                            df[col] = self._handle_missing(df, col, issue["strategy"])
                elif issue["type"] == "outliers":
                    for col in issue["columns"]:
                        df = self._remove_outliers(df, col, issue["strategy"])
                elif issue["type"] == "duplicates":
                    if issue["strategy"] == "keep_first":
                        df = df.drop_duplicates(keep='first')
            
            print(f"AI分析结果：{analysis.get('recommendations', [])}")
            
        except json.JSONDecodeError:
            print("AI解析失败，使用默认清洗规则")
            df = self._apply_default_rules(df)
        
        return df
    
    def _handle_missing(self, df: pd.DataFrame, column: str, strategy: str):
        """处理缺失值"""
        if strategy == "mean":
            df[column] = df[column].fillna(df[column].mean())
        elif strategy == "median":
            df[column] = df[column].fillna(df[column].median())
        elif strategy == "mode":
            df[column] = df[column].fillna(df[column].mode()[0])
        elif strategy == "drop":
            df = df.dropna(subset=[column])
        else:
            df[column] = df[column].fillna(strategy)
