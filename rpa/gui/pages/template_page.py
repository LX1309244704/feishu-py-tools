"""
模板市场页面
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel,
    QPushButton, QLineEdit, QComboBox, QHBoxLayout
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt


class TemplateCard(QFrame):
    """模板卡片组件"""
    
    def __init__(self, name: str, description: str, category: str, color: str):
        super().__init__()
        self.name = name
        self.description = description
        self.category = category
        self.color = color
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            TemplateCard {{
                background-color: {color};
                border-radius: 12px;
                padding: 20px;
            }}
            QLabel {{
                color: white;
            }}
        """)
        self.setFixedHeight(150)
        
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel(f"<h3>{name}</h3>")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        
        # 分类
        category_label = QLabel(f"📁 {category}")
        category_label.setStyleSheet("opacity: 0.8; font-size: 12px;")
        
        # 描述
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("opacity: 0.9;")
        
        # 使用按钮
        use_btn = QPushButton("使用模板")
        use_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        use_btn.clicked.connect(self._on_use)
        
        layout.addWidget(title_label)
        layout.addWidget(category_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(use_btn, alignment=Qt.AlignRight)
    
    def _on_use(self):
        """使用模板"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "使用模板", f"使用模板：{self.name}")


class TemplatePage(QWidget):
    """模板市场页面"""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 顶部搜索栏
        search_layout = QHBoxLayout()
        
        search_label = QLabel("<h2>📦 模板市场</h2>")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索模板...")
        self.search_input.setFixedWidth(300)
        
        category_label = QLabel("分类：")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["全部", "办公自动化", "数据处理", "消息通知", "系统集成"])
        
        search_layout.addWidget(search_label)
        search_layout.addStretch()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(category_label)
        search_layout.addWidget(self.category_combo)
        
        main_layout.addLayout(search_layout)
        
        # 模板网格
        self.templates_grid = QGridLayout()
        self.templates_grid.setSpacing(20)
        
        # 模板数据
        templates = [
            ("库存预警流程", "每2小时检查库存，低于最小库存发送预警通知", "办公自动化", "#e74c3c"),
            ("每日销售报表", "工作日18点自动生成销售报表并发送群通知", "办公自动化", "#3498db"),
            ("新员工入职流程", "自动创建飞书账号，发送入职指引，加入部门群", "办公自动化", "#2ecc71"),
            ("数据同步流程", "飞书多维表格和业务系统数据自动同步", "系统集成", "#f39c12"),
            ("考勤提醒流程", "上下班自动发送上下班打卡提醒，统计考勤数据", "办公自动化", "#9b59b6"),
            ("周报生成流程", "每周五自动汇总工作内容生成周报", "办公自动化", "#1abc9c"),
            ("客户跟进提醒", "定期提醒跟进客户，记录跟进内容", "办公自动化", "#e67e22"),
            ("数据备份流程", "定期备份飞书数据到本地或云存储", "数据处理", "#34495e"),
        ]
        
        for i, (name, desc, category, color) in enumerate(templates):
            card = TemplateCard(name, desc, category, color)
            self.templates_grid.addWidget(card, i // 4, i % 4)
        
        main_layout.addLayout(self.templates_grid)
        main_layout.addStretch()
