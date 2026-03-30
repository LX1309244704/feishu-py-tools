"""
设置页面
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QGroupBox, QCheckBox, QComboBox,
    QFileDialog, QMessageBox, QHBoxLayout, QLabel
)
from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon


class SettingsPage(QWidget):
    """设置页面"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings("FeishuTools", "RPA Client")
        self._init_ui()
        self._load_settings()
    
    def _init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("<h2>⚙️ 系统设置</h2>")
        main_layout.addWidget(title_label)
        
        # 飞书配置
        feishu_group = QGroupBox("飞书应用配置")
        feishu_layout = QFormLayout(feishu_group)
        
        self.app_id_input = QLineEdit()
        self.app_id_input.setPlaceholderText("cli_xxxxxx")
        self.app_secret_input = QLineEdit()
        self.app_secret_input.setPlaceholderText("xxxxxx")
        self.app_secret_input.setEchoMode(QLineEdit.Password)
        
        feishu_layout.addRow("App ID：", self.app_id_input)
        feishu_layout.addRow("App Secret：", self.app_secret_input)
        
        main_layout.addWidget(feishu_group)
        
        # 通用配置
        general_group = QGroupBox("通用设置")
        general_layout = QFormLayout(general_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["自动", "亮色主题", "深色主题"])
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["简体中文", "English"])
        
        self.startup_check = QCheckBox("开机自动启动")
        self.minimize_check = QCheckBox("启动时最小化到托盘")
        self.auto_save_check = QCheckBox("自动保存编辑的流程")
        
        general_layout.addRow("主题：", self.theme_combo)
        general_layout.addRow("语言：", self.lang_combo)
        general_layout.addRow(self.startup_check)
        general_layout.addRow(self.minimize_check)
        general_layout.addRow(self.auto_save_check)
        
        main_layout.addWidget(general_group)
        
        # 路径配置
        path_group = QGroupBox("路径配置")
        path_layout = QFormLayout(path_group)
        
        self.flow_path_input = QLineEdit()
        self.flow_path_browse_btn = QPushButton("浏览")
        self.flow_path_browse_btn.clicked.connect(self._browse_flow_path)
        flow_path_layout = QHBoxLayout()
        flow_path_layout.addWidget(self.flow_path_input)
        flow_path_layout.addWidget(self.flow_path_browse_btn)
        
        self.log_path_input = QLineEdit()
        self.log_path_browse_btn = QPushButton("浏览")
        self.log_path_browse_btn.clicked.connect(self._browse_log_path)
        log_path_layout = QHBoxLayout()
        log_path_layout.addWidget(self.log_path_input)
        log_path_layout.addWidget(self.log_path_browse_btn)
        
        path_layout.addRow("流程默认保存路径：", flow_path_layout)
        path_layout.addRow("日志保存路径：", log_path_layout)
        
        main_layout.addWidget(path_group)
        
        # 保存按钮
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton(QIcon(":/icons/save.png"), "保存设置")
        self.save_btn.setStyleSheet("""
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
        self.save_btn.clicked.connect(self._save_settings)
        
        self.reset_btn = QPushButton("恢复默认")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.reset_btn.clicked.connect(self._reset_settings)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.reset_btn)
        main_layout.addLayout(btn_layout)
        
        main_layout.addStretch()
    
    def _load_settings(self):
        """加载设置"""
        self.app_id_input.setText(self.settings.value("feishu/app_id", ""))
        self.app_secret_input.setText(self.settings.value("feishu/app_secret", ""))
        
        theme_index = self.settings.value("general/theme", 0)
        self.theme_combo.setCurrentIndex(int(theme_index))
        
        lang_index = self.settings.value("general/language", 0)
        self.lang_combo.setCurrentIndex(int(lang_index))
        
        self.startup_check.setChecked(self.settings.value("general/startup", False, type=bool))
        self.minimize_check.setChecked(self.settings.value("general/minimize", False, type=bool))
        self.auto_save_check.setChecked(self.settings.value("general/auto_save", True, type=bool))
        
        self.flow_path_input.setText(self.settings.value("path/flows", ""))
        self.log_path_input.setText(self.settings.value("path/logs", ""))
    
    def _save_settings(self):
        """保存设置"""
        self.settings.setValue("feishu/app_id", self.app_id_input.text())
        self.settings.setValue("feishu/app_secret", self.app_secret_input.text())
        
        self.settings.setValue("general/theme", self.theme_combo.currentIndex())
        self.settings.setValue("general/language", self.lang_combo.currentIndex())
        self.settings.setValue("general/startup", self.startup_check.isChecked())
        self.settings.setValue("general/minimize", self.minimize_check.isChecked())
        self.settings.setValue("general/auto_save", self.auto_save_check.isChecked())
        
        self.settings.setValue("path/flows", self.flow_path_input.text())
        self.settings.setValue("path/logs", self.log_path_input.text())
        
        self.settings.sync()
        QMessageBox.information(self, "保存成功", "设置已保存，部分设置需要重启生效！")
    
    def _reset_settings(self):
        """恢复默认设置"""
        reply = QMessageBox.question(
            self, "确认恢复", "确定要恢复所有设置为默认值吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.settings.clear()
            self._load_settings()
            QMessageBox.information(self, "恢复成功", "设置已恢复为默认值！")
    
    def _browse_flow_path(self):
        """浏览流程路径"""
        path = QFileDialog.getExistingDirectory(self, "选择流程保存路径")
        if path:
            self.flow_path_input.setText(path)
    
    def _browse_log_path(self):
        """浏览日志路径"""
        path = QFileDialog.getExistingDirectory(self, "选择日志保存路径")
        if path:
            self.log_path_input.setText(path)
