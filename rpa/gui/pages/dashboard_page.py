"""
首页仪表盘页面
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QFont, QColor, QIcon
from PySide6.QtCore import Qt, QDateTime


class StatCard(QFrame):
    """统计卡片组件"""
    
    def __init__(self, title: str, value: str, icon: str, color: str = "#3498db"):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            StatCard {{
                background-color: {color};
                border-radius: 12px;
                padding: 20px;
            }}
            QLabel {{
                color: white;
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel(title)
        title_label.setFont(QFont("Microsoft YaHei", 10))
        title_label.setStyleSheet("font-weight: normal; opacity: 0.9;")
        
        # 数值
        value_label = QLabel(value)
        value_label.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        
        # 布局
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        self.setFixedHeight(120)


class DashboardPage(QWidget):
    """首页仪表盘页面"""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._load_data()
    
    def _init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 顶部欢迎区域
        welcome_layout = QHBoxLayout()
        
        welcome_text = QLabel("<h1>🤖 RPA机器人流程自动化工具</h1>")
        welcome_text.setOpenExternalLinks(True)
        
        datetime_label = QLabel(f"欢迎使用！当前时间：{QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss")
        datetime_label.setStyleSheet("color: #666; font-size: 14px;")
        
        welcome_layout.addWidget(welcome_text)
        welcome_layout.addStretch()
        
        # 快捷操作按钮
        new_flow_btn = QPushButton(QIcon(":/icons/new.png"), "新建流程")
        new_flow_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        new_flow_btn.clicked.connect(self._on_new_flow)
        welcome_layout.addWidget(new_flow_btn)
        
        run_flow_btn = QPushButton(QIcon(":/icons/run.png"), "执行流程")
        run_flow_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        run_flow_btn.clicked.connect(self._on_run_flow)
        welcome_layout.addWidget(run_flow_btn)
        
        main_layout.addLayout(welcome_layout)
        main_layout.addWidget(datetime_label)
        
        # 统计卡片区域
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)
        
        # 统计卡片
        self.total_flow_card = StatCard("总流程数", "12", ":/icons/flow.png", "#3498db")
        self.today_run_card = StatCard("今日执行", "8", ":/icons/run.png", "#2ecc71")
        self.success_rate_card = StatCard("成功率", "92%", ":/icons/success.png", "#f39c12")
        self.avg_time_card = StatCard("平均耗时", "4.2s", ":/icons/time.png", "#9b59b6")
        
        stats_layout.addWidget(self.total_flow_card, 0, 0)
        stats_layout.addWidget(self.today_run_card, 0, 1)
        stats_layout.addWidget(self.success_rate_card, 0, 2)
        stats_layout.addWidget(self.avg_time_card, 0, 3)
        
        main_layout.addLayout(stats_layout)
        
        # 最近执行记录区域
        recent_layout = QVBoxLayout()
        recent_title = QLabel("<h3>最近执行记录</h3>")
        recent_layout.addWidget(recent_title)
        
        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(5)
        self.recent_table.setHorizontalHeaderLabels(["流程名称", "执行时间", "状态", "耗时", "操作"])
        self.recent_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.recent_table.setAlternatingRowColors(True)
        self.recent_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # 加载示例数据
        self._load_recent_records()
        
        recent_layout.addWidget(self.recent_table)
        main_layout.addLayout(recent_layout)
        
        # 常用模板区域
        template_layout = QVBoxLayout()
        template_title = QLabel("<h3>常用模板</h3>")
        template_layout.addWidget(template_title)
        
        # 模板卡片
        template_grid = QGridLayout()
        template_grid.setSpacing(15)
        
        templates = [
            ("库存预警流程", "每2小时检查库存，低于阈值发送预警", "#e74c3c"),
            ("每日销售报表", "工作日18点自动生成报表", "#3498db"),
            ("新员工入职流程", "自动创建账号，发送入职指引", "#2ecc71"),
            ("数据同步流程", "飞书和业务系统数据同步", "#f39c12")
        ]
        
        for i, (name, desc, color) in enumerate(templates):
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {color};
                    border-radius: 8px;
                    padding: 15px;
                }}
                QLabel {{
                    color: white;
                }}
            """)
            card.setFixedHeight(100)
            
            layout = QVBoxLayout(card)
            name_label = QLabel(f"<b>{name}</b>")
            name_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("opacity: 0.9;")
            use_btn = QPushButton("使用模板")
            use_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 4px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                }
            """)
            use_btn.clicked.connect(lambda _, n=name: self._use_template(n))
            
            layout.addWidget(name_label)
            layout.addWidget(desc_label)
            layout.addStretch()
            layout.addWidget(use_btn, alignment=Qt.AlignRight)
            
            template_grid.addWidget(card, i // 2, i % 2)
        
        template_layout.addLayout(template_grid)
        main_layout.addLayout(template_layout)
        
        main_layout.addStretch()
    
    def _load_data(self):
        """加载统计数据"""
        # 后续从本地存储加载
        pass
    
    def _load_recent_records(self):
        """加载最近执行记录"""
        records = [
            ("库存预警流程", "2026-03-30 08:00:00", "成功", "2.3s"),
            ("销售报表生成", "2026-03-29 18:00:00", "成功", "15.6s"),
            ("数据同步流程", "2026-03-29 16:00:00", "成功", "8.1s"),
            ("考勤提醒", "2026-03-29 09:00:00", "成功", "1.5s"),
            ("库存预警流程", "2026-03-29 08:00:00", "失败", "3.2s"),
        ]
        
        self.recent_table.setRowCount(len(records))
        for i, (name, time, status, duration) in enumerate(records):
            self.recent_table.setItem(i, 0, QTableWidgetItem(name))
            self.recent_table.setItem(i, 1, QTableWidgetItem(time))
            
            status_item = QTableWidgetItem(status)
            if status == "成功":
                status_item.setForeground(QColor("#27ae60"))
                status_item.setBackground(QColor("#f0f9f4"))
            else:
                status_item.setForeground(QColor("#e74c3c"))
                status_item.setBackground(QColor("#fdf2f2"))
            self.recent_table.setItem(i, 2, status_item)
            
            self.recent_table.setItem(i, 3, QTableWidgetItem(duration))
            
            # 操作按钮
            btn = QPushButton("重新执行")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn.clicked.connect(lambda _, n=name: self._rerun_flow(n))
            self.recent_table.setCellWidget(i, 4, btn)
    
    def _on_new_flow(self):
        """新建流程按钮点击"""
        from PySide6.QtWidgets.QApplication.instance().activeWindow().tab_widget.setCurrentIndex(1)
    
    def _on_run_flow(self):
        """执行流程按钮点击"""
        # 后续实现打开流程选择
        pass
    
    def _rerun_flow(self, flow_name):
        """重新执行流程"""
        # 后续实现
        from PySide6.QtWidgets.QMessageBox.information(self, "执行", f"重新执行流程: {flow_name}")
    
    def _use_template(self, template_name):
        """使用模板"""
        # 后续实现
        from PySide6.QtWidgets.QMessageBox.information(self, "模板", f"使用模板: {template_name}")
