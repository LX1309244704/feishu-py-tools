"""
执行记录页面
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QLineEdit, QLabel, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class ExecutionPage(QWidget):
    """执行记录页面"""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 顶部搜索栏
        search_layout = QHBoxLayout()
        
        search_label = QLabel("搜索：")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入流程名称搜索...")
        self.search_input.textChanged.connect(self._filter_records)
        
        status_label = QLabel("状态：")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["全部", "成功", "失败"])
        self.status_combo.currentTextChanged.connect(self._filter_records)
        
        clear_btn = QPushButton("清空")
        clear_btn.clicked.connect(self._clear_filter)
        
        export_btn = QPushButton("导出记录")
        export_btn.clicked.connect(self._export_records)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(status_label)
        search_layout.addWidget(self.status_combo)
        search_layout.addWidget(clear_btn)
        search_layout.addStretch()
        search_layout.addWidget(export_btn)
        
        main_layout.addLayout(search_layout)
        
        # 记录表格
        self.record_table = QTableWidget()
        self.record_table.setColumnCount(6)
        self.record_table.setHorizontalHeaderLabels([
            "流程名称", "开始时间", "结束时间", "耗时", "状态", "操作"
        ])
        self.record_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.record_table.setAlternatingRowColors(True)
        self.record_table.setStyleSheet("""
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
        self._load_records()
        
        main_layout.addWidget(self.record_table)
    
    def _load_records(self):
        """加载执行记录"""
        records = [
            ("库存预警流程", "2026-03-30 08:00:00", "2026-03-30 08:00:02", "2.3s", "成功"),
            ("销售报表生成", "2026-03-29 18:00:00", "2026-03-29 18:00:15", "15.6s", "成功"),
            ("数据同步流程", "2026-03-29 16:00:00", "2026-03-29 16:00:08", "8.1s", "成功"),
            ("考勤提醒", "2026-03-29 09:00:00", "2026-03-29 09:00:01", "1.5s", "成功"),
            ("库存预警流程", "2026-03-29 08:00:00", "2026-03-29 08:00:03", "3.2s", "失败"),
            ("周报生成流程", "2026-03-29 17:00:00", "2026-03-29 17:00:10", "10.2s", "成功"),
            ("客户跟进提醒", "2026-03-29 10:00:00", "2026-03-29 10:00:02", "2.1s", "成功"),
        ]
        
        self.record_table.setRowCount(len(records))
        for i, (name, start, end, duration, status) in enumerate(records):
            self.record_table.setItem(i, 0, QTableWidgetItem(name))
            self.record_table.setItem(i, 1, QTableWidgetItem(start))
            self.record_table.setItem(i, 2, QTableWidgetItem(end))
            self.record_table.setItem(i, 3, QTableWidgetItem(duration))
            
            status_item = QTableWidgetItem(status)
            if status == "成功":
                status_item.setForeground(QColor("#27ae60"))
                status_item.setBackground(QColor("#f0f9f4"))
            else:
                status_item.setForeground(QColor("#e74c3c"))
                status_item.setBackground(QColor("#fdf2f2"))
            self.record_table.setItem(i, 4, status_item)
            
            # 操作按钮
            btn_layout = QHBoxLayout()
            rerun_btn = QPushButton("重新执行")
            rerun_btn.setStyleSheet("""
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
            rerun_btn.clicked.connect(lambda _, n=name: self._rerun_flow(n))
            
            detail_btn = QPushButton("详情")
            detail_btn.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #7f8c8d;
                }
            """)
            detail_btn.clicked.connect(lambda _, n=name: self._show_detail(n))
            
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.addWidget(rerun_btn)
            btn_layout.addWidget(detail_btn)
            self.record_table.setCellWidget(i, 5, btn_widget)
    
    def _filter_records(self):
        """过滤记录"""
        search_text = self.search_input.text().lower()
        status_filter = self.status_combo.currentText()
        
        for i in range(self.record_table.rowCount()):
            name = self.record_table.item(i, 0).text().lower()
            status = self.record_table.item(i, 4).text()
            
            match_search = search_text in name
            match_status = (status_filter == "全部") or (status == status_filter)
            
            self.record_table.setRowHidden(i, not (match_search and match_status))
    
    def _clear_filter(self):
        """清空过滤"""
        self.search_input.clear()
        self.status_combo.setCurrentIndex(0)
    
    def _export_records(self):
        """导出记录"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "导出", "导出功能开发中...")
    
    def _rerun_flow(self, flow_name):
        """重新执行流程"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "执行", f"重新执行流程：{flow_name}")
    
    def _show_detail(self, flow_name):
        """查看详情"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "详情", f"查看流程执行详情：{flow_name}")
