"""
插件中心页面
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QLabel, QLineEdit, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class PluginPage(QWidget):
    """插件中心页面"""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 顶部标题
        top_layout = QHBoxLayout()
        title_label = QLabel("<h2>🔌 插件中心</h2>")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索插件...")
        self.search_input.setFixedWidth(300)
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.search_input)
        main_layout.addLayout(top_layout)
        
        # 标签页
        tab_widget = QTabWidget()
        
        # 已安装插件列表
        installed_tab = QWidget()
        installed_layout = QVBoxLayout(installed_tab)
        
        self.installed_table = QTableWidget()
        self.installed_table.setColumnCount(5)
        self.installed_table.setHorizontalHeaderLabels(["插件名称", "版本", "描述", "作者", "操作"])
        self.installed_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.installed_table.setAlternatingRowColors(True)
        
        # 加载已安装插件
        self._load_installed_plugins()
        installed_layout.addWidget(self.installed_table)
        tab_widget.addTab(installed_tab, "已安装插件")
        
        # 在线插件市场
        market_tab = QWidget()
        market_layout = QVBoxLayout(market_tab)
        coming_label = QLabel("<h2>🚧 插件市场正在开发中...</h2>")
        coming_label.setAlignment(Qt.AlignCenter)
        market_layout.addWidget(coming_label)
        tab_widget.addTab(market_tab, "插件市场")
        
        main_layout.addWidget(tab_widget)
    
    def _load_installed_plugins(self):
        """加载已安装插件"""
        from rpa.core.plugin import list_plugins
        plugins = list_plugins()
        
        self.installed_table.setRowCount(len(plugins))
        for i, plugin in enumerate(plugins):
            self.installed_table.setItem(i, 0, QTableWidgetItem(plugin['name']))
            self.installed_table.setItem(i, 1, QTableWidgetItem(plugin['version']))
            self.installed_table.setItem(i, 2, QTableWidgetItem(plugin['description']))
            self.installed_table.setItem(i, 3, QTableWidgetItem(plugin['author']))
            
            # 操作按钮
            detail_btn = QPushButton("详情")
            detail_btn.setStyleSheet("""
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
            detail_btn.clicked.connect(lambda _, p=plugin: self._show_detail(p))
            
            self.installed_table.setCellWidget(i, 4, detail_btn)
    
    def _show_detail(self, plugin):
        """显示插件详情"""
        from PySide6.QtWidgets import QMessageBox
        detail_text = f"""
插件名称：{plugin['name']}
版本：{plugin['version']}
描述：{plugin['description']}
作者：{plugin['author']}
"""
        QMessageBox.information(self, "插件详情", detail_text)
