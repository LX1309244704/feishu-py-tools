"""
数据可视化模块
"""
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json


class DataVisualizer:
    """数据可视化器"""
    
    def __init__(self, style: str = "plotly"):
        """
        初始化可视化器
        
        Args:
            style: 样式（plotly/plotly_express）
        """
        self.style = style
        
        # 配置Plotly主题
        if style == "plotly":
            px.defaults.template = "plotly"
            self.theme = "plotly_white"
        else:
            plt.style.use('seaborn-v0_8-dark')
        
        # 配置中文字
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
    
    def create_dashboard(self, data: List[Dict[str, Any]], 
                      layout: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        创建仪表盘
        
        Args:
            data: 数据列表
            layout: 布局配置
            
        Returns:
            仪表盘信息
        """
        if not data:
            return {"success": False, "error": "数据不能为空"}
        
        try:
            if not layout:
                layout = self._auto_layout(data)
            
            print(f"创建仪表盘，数据条数：{len(data)}")
            
            if self.style == "plotly":
                fig = self._create_plotly_dashboard(data, layout)
            else:
                fig = self._create_matplotlib_dashboard(data, layout)
            
            return {
                "success": True,
                "dashboard_type": self.style,
                "data_count": len(data),
                "layout": layout
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"创建仪表盘失败: {str(e)}"
            }
    
    def _auto_layout(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        自动布局生成
        
        Args:
            data: 数据列表
            
        Returns:
            布局配置
        """
        # 自动识别数据类型
        numeric_cols = []
        categorical_cols = []
        
        if data and isinstance(data[0], dict):
            for col in data[0].keys():
                value = data[0][col]
                if isinstance(value, (int, float)):
                    numeric_cols.append(col)
                elif isinstance(value, str):
                    categorical_cols.append(col)
        
        layout = {
            "rows": 1,
            "columns": len(data[0].keys()) if data else 1,
            "size": 4,
            "graph_type": "table",
            "type": "table",
            "data": data,
            "size": len(data),
            "start": 0,
            "end": len(data),
            "row_height": 60,
            "title": "飞书数据看板",
            "row_title": list(data[0].keys()) if data else [],
            "numeric_cols": numeric_cols,
            "categorical_cols": categorical_cols
        }
        
        return layout
    
    def _create_plotly_dashboard(self, data: List[Dict[str, Any]],
                             layout: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        创建Plotly仪表盘
        
        Args:
            data: 数据列表
            layout: 布局配置
            
        Returns:
            仪表盘信息
        """
        if not layout:
            layout = self._auto_layout(data)
        
        numeric_cols = layout.get("numeric_cols", [])
        categorical_cols = layout.get("categorical_cols", [])
        
        # 创建子图
        graphs = []
        
        # 图1: 数据分布（饼图）
        if len(categorical_cols) > 0 and len(data) > 0:
            col = categorical_cols[0]
            cat_counts = {}
            for item in data:
                value = item.get(col, "未知")
                cat_counts[value] = cat_counts.get(value, 0) + 1
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(cat_counts.keys()),
                values=list(cat_counts.values()),
                hole=.5
            )])
            fig_pie.update_traces(
                textposition='inside',
                textinfo='label+percent',
                textfont_size=14
            )
            fig_pie.update_layout(title=f"{col}分布")
            graphs.append(fig_pie)
        
        # 图2: 数值分布（柱状图）
        if len(numeric_cols) > 0 and len(data) > 0:
            for col in numeric_cols[:3]:  # 最多3个数值列
                values = [item.get(col, 0) for item in data]
                fig_bar = go.Figure(data=[go.Bar(x=list(range(len(data))), y=values, name=col)])
                fig_bar.update_traces(
                    marker_line_color="lightgray"
                )
                fig_bar.update_layout(
                    title=f"{col}统计",
                    xaxis_title="索引",
                    yaxis_title="值"
                )
                graphs.append(fig_bar)
        
        # 图3: 数据统计（表格）
        if data:
            table_values = [[str(item.get(col, "")) for col in data[0].keys()] for item in data[:10]]
            fig_table = go.Figure(data=[go.Table(
                header=dict(
                    values=list(data[0].keys()),
                    fill_color='lightyellow'
                ),
                cells=dict(
                    values=zip(*table_values) if len(table_values) > 0 else [],
                    align='center',
                    font=dict(size=12)
                )
            )])
            fig_table.update_layout(title="数据表（前10条）", height=400)
            graphs.append(fig_table)
        
        # 图4: 数据趋势（折线图）
        if len(numeric_cols) > 1 and len(data) > 0:
            fig_line = go.Figure()
            times = list(range(len(data)))
            for col in numeric_cols[:2]:  # 最多2个数值列
                values = [item.get(col, 0) for item in data]
                fig_line.add_trace(
                    go.Scatter(
                        x=times,
                        y=values,
                        mode='lines+markers',
                        name=col
                    )
                )
            
            fig_line.update_layout(
                title="数据趋势",
                xaxis_title="索引",
                yaxis_title="值"
            )
            graphs.append(fig_line)
        
        return {
            "success": True,
            "dashboard_type": "plotly",
            "graphs": len(graphs),
            "graph_names": [f"{i+1}. {g.layout.title.text if hasattr(g, 'layout') else '图表'}" for i, g in enumerate(graphs)]
        }
    
    def _create_matplotlib_dashboard(self, data: List[Dict[str, Any]],
                                 layout: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        创建Matplotlib仪表盘
        
        Args:
            data: 数据列表
            layout: 布局配置
            
        Returns:
            仪表盘信息
        """
        if not layout:
            layout = self._auto_layout(data)
        
        numeric_cols = layout.get("numeric_cols", [])
        categorical_cols = layout.get("categorical_cols", [])
        
        # 创建子图
        n_cols = min(4, len(data[0].keys()) if data else 1)
        n_rows = 1
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 8))
        if n_cols == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        fig.suptitle("飞书数据看板", fontsize=16)
        fig.patch.set_facecolor('#f8f9fa')
        
        # 绘制图表
        idx = 0
        
        # 饼图1：数据分布
        if len(categorical_cols) > 0 and len(data) > 0 and idx < len(axes):
            col = categorical_cols[0]
            cat_counts = {}
            for item in data:
                value = item.get(col, "未知")
                cat_counts[value] = cat_counts.get(value, 0) + 1
            
            colors = ['#667eea', '#764ba2', '#f39c12', '#e74c3c', '#00b894', '#FFA07A']
            axes[idx].pie(cat_counts.values(), labels=cat_counts.keys(), autopct='%1.1f%%', colors=colors)
            axes[idx].set_title(f'{col}分布', fontweight=600)
            idx += 1
        
        # 柱状图：数值统计
        if len(numeric_cols) > 0 and len(data) > 0 and idx < len(axes):
            col = numeric_cols[0]
            values = [item.get(col, 0) for item in data[:10]]
            axes[idx].bar(range(len(values)), values, color=colors[0])
            axes[idx].set_title(f'{col}统计', fontweight=600)
            axes[idx].set_xlabel('索引')
            axes[idx].set_ylabel('值')
            axes[idx].grid(True, alpha=0.3)
            idx += 1
        
        # 数据表
        if data and idx < len(axes):
            axes[idx].axis('off')
            table_data = [[str(item.get(col, "")) for col in data[0].keys()] for item in data[:10]]
            table = axes[idx].table(cellText=table_data, colLabels=list(data[0].keys()),
                                 cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            axes[idx].set_title('数据表（前10条）', fontweight=600)
            idx += 1
        
        # 折线图：数据趋势
        if len(numeric_cols) > 1 and len(data) > 0 and idx < len(axes):
            col = numeric_cols[0]
            values = [item.get(col, 0) for item in data]
            axes[idx].plot(range(len(values)), values, marker='o', color=colors[1])
            axes[idx].set_title(f'{col}趋势', fontweight=600)
            axes[idx].set_xlabel('索引')
            axes[idx].set_ylabel('值')
            axes[idx].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        return {
            "success": True,
            "dashboard_type": "matplotlib",
            "rows": n_rows,
            "columns": n_cols
        }
    
    def create_chart(self, data: Dict[str, Any], 
                   chart_type: str = "bar",
                   title: str = "图表标题",
                   x: str = None, y: str = None) -> str:
        """
        创建图表
        
        Args:
            data: 数据字典
            chart_type: 图表类型（bar/line/pie/scatter/area）
            title: 图表标题
            x: x轴字段
            y: y轴字段
            
        Returns:
            图表信息或文件路径
        """
        if chart_type == "bar":
            return self._create_bar_chart(data, title, x, y)
        elif chart_type == "line":
            return self._create_line_chart(data, title, x, y)
        elif chart_type == "pie":
            return self._create_pie_chart(data, title)
        elif chart_type == "scatter":
            return self._create_scatter_chart(data, title, x, y)
        else:
            raise ValueError(f"不支持的图表类型: {chart_type}")
    
    def _create_bar_chart(self, data: Dict[str, Any], title: str, x: str = None, 
                     y: str = None) -> str:
        """创建柱状图"""
        fig = px.bar(data, x=x, y=y, title=title, color_discrete_sequence=["#667eea", "#764ba2", "#f39c12"], 
                       hover_data=data, labels=x)
        
        return self._save_chart(fig, title, f"bar_chart_{len(data)}")
    
    def _create_line_chart(self, data: Dict[str, Any], title: str, x: str = None, 
                      y: str = None) -> str:
        """创建折线图"""
        fig = px.line(data, x=x, y=y, title=title, markers=True,
                        hover_data=data, labels=x, template="lines+markers")
        
        return self._save_chart(fig, title, f"line_chart_{len(data)}")
    
    def _create_pie_chart(self, data: Dict[str, Any], title: str) -> str:
        """创建饼图"""
        fig = px.pie(data, names=title, title=title,
                       color_discrete_sequence=["#667eea", "#764ba2", "#f39c12"])
        
        return self._save_chart(fig, title, f"pie_chart_{len(data)}")
    
    def _create_scatter_chart(self, data: Dict[str, Any], title: str, 
                           x: str = None, y: str = None) -> str:
        """创建散点图"""
        fig = px.scatter(data, x=x, y=y, title=title, color="color",
                          hover_data=data, hover_name=x, template="plotly_white")
        
        return self._save_chart(fig, title, f"scatter_chart_{len(data)}")
    
    def _save_chart(self, fig, title: str, filename: str) -> str:
        """保存图表"""
        filename = f"{title.replace(' ', '_')}.png"
        fig.write_image(filename)
        return filename
    
    def create_heatmap(self, data: pd.DataFrame, title: str,
                     x: str = None, y: str = None) -> str:
        """
        创建热力图

        Args:
            data: DataFrame数据
            title: 标题
            x: x轴字段
            y: y轴字段

        Returns:
            文件路径
        """
        if x and y:
            pivot_table = data.pivot_table(index=y, columns=x)
        else:
            pivot_table = data.T

        fig = px.imshow(pivot_table,
                            title=title,
                            color_continuous_scale='Blues',
                            title_font=dict(size=14),
                            height=600)
        fig.update_xaxis(title=x or "", title_font=dict(size=12))
        fig.update_yaxis(title=y or "", title_font=dict(size=12))

        return self._save_chart(fig, title, f"heatmap_{len(data)}")
    
    def create_histogram(self, data: pd.DataFrame, column: str,
                       title: str, bins: int = 10) -> str:
        """
        创建直方图

        Args:
            data: DataFrame数据
            column: 列名
            title: 标题
            bins: 分箱数

        Returns:
            文件路径
        """
        fig = px.histogram(data, x=column, title=title, nbins=bins,
                          color_discrete_sequence=["#667eea", "#764ba2", "#f39c12"])
        return self._save_chart(fig, title, f"histogram_{column}_{len(data)}")
    
    def save_report(self, data: pd.DataFrame,
                   title: str, filename: str = None) -> str:
        """
        生成报告

        Args:
            data: DataFrame数据
            title: 报告标题
            filename: 文件名

        Returns:
            报告文件路径
        """
        if filename is None:
            filename = f"{title.replace(' ', '_')}.xlsx"

        with pd.ExcelWriter(filename) as writer:
            data.to_excel(writer, index=False, sheet_name=title)

        return filename
    
    def export_chart(self, fig, filename: str = None) -> str:
        """
        导出图表

        Args:
            fig: Plotly图表对象
            filename: 文件名

        Returns:
            文件路径
        """
        if filename is None:
            filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        filename = filename.replace(' ', '_') + '.png'
        fig.write_image(filename)
        return filename
    
    def export_dashboard(self, fig, html_filename: str = "dashboard.html") -> str:
        """
        导出仪表盘为HTML

        Args:
            fig: 图表对象
            html_filename: HTML文件名

        Returns:
            文件路径
        """
        if self.style == "plotly":
            import plotly.graph_objects as go
            html_file = html_filename
            fig.write_html(html_file)
        else:
            import matplotlib.pyplot as plt
            html_file = html_filename.replace('.html', '_matplotlib.html')
            fig.savefig(html_file, bbox_inches='tight')

        return html_file
    
    def create_simple_dashboard(self, data: pd.DataFrame,
                             row_count: int = 5) -> str:
        """
        创建简单仪表盘
        
        Args:
            data: DataFrame数据
            row_count: 显示的行数
            
        """
        if len(data) == 0:
            return "没有数据"
        
        data_sample = data.head(row_count)
        
        fig = plt.figure(figsize=(15, 8))
        fig.suptitle('飞书数据看板', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # 只显示数值列
        numeric_cols = data_sample.select_dtypes(include=['number']).columns
        
        for i, col in enumerate(numeric_cols[:4]):  # 最多显示4个数值列
            ax = fig.add_subplot(2, 2, i + 1)
            ax.bar(data_sample[col])
            ax.set_title(col, fontweight=600)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = f"simple_dashboard_{len(data)}_{row_count}.png"
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        return filename
    
    def show_dashboard(self, fig = None):
        """显示仪表盘"""
        if fig is None:
            print("没有图表可显示")
            return
        
        plt.show()
    
    def close_dashboard(self):
        """关闭仪表盘"""
        plt.close('all')
        print("仪表盘已关闭")
