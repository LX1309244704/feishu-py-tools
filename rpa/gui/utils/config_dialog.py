"""
配置对话框
所有配置都在GUI中完成
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QLineEdit, QPushButton, QFormLayout,
    QMessageBox, QFileDialog, QWidget, QGroupBox,
    QComboBox, QCheckBox
)
from PySide6.QtCore import Qt

from .config_manager import get_config


class ConfigDialog(QDialog):
    """配置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置管理 - 微元Weiyuan")
        self.resize(700, 600)
        self.config = get_config()
        
        self._init_ui()
        self._load_config()
    
    def _init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标签页
        self.tab_widget = QTabWidget()
        
        # 飞书配置页
        self.tab_widget.addTab(self._create_feishu_tab(), "飞书")
        
        # 企业微信配置页
        self.tab_widget.addTab(self._create_wechat_work_tab(), "企业微信")
        
        # 公众号配置页
        self.tab_widget.addTab(self._create_wechat_mp_tab(), "公众号")
        
        # AI配置页
        self.tab_widget.addTab(self._create_ai_tab(), "AI大模型")
        
        # 通用配置页
        self.tab_widget.addTab(self._create_general_tab(), "通用")
        
        layout.addWidget(self.tab_widget)
        
        # 底部按钮
        btn_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("保存配置")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.save_btn.clicked.connect(self._save_config)
        
        self.test_btn = QPushButton("测试连接")
        self.test_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.test_btn.clicked.connect(self._test_connection)
        
        self.reset_btn = QPushButton("重置默认")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.reset_btn.clicked.connect(self._reset_config)
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(self.test_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_btn)
        btn_layout.addWidget(self.save_btn)
        
        layout.addLayout(btn_layout)
    
    def _create_feishu_tab(self) -> QWidget:
        """创建飞书配置页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        group = QGroupBox("飞书应用配置")
        group_layout = QFormLayout(group)
        
        self.feishu_app_id = QLineEdit()
        self.feishu_app_id.setPlaceholderText("cli_xxxxxx")
        group_layout.addRow("App ID:", self.feishu_app_id)
        
        self.feishu_app_secret = QLineEdit()
        self.feishu_app_secret.setPlaceholderText("输入你的App Secret")
        self.feishu_app_secret.setEchoMode(QLineEdit.Password)
        group_layout.addRow("App Secret:", self.feishu_app_secret)
        
        # 添加说明
        help_label = QLabel("💡 提示：在飞书开放平台创建应用，获取App ID和App Secret")
        help_label.setStyleSheet("color: #666; font-size: 12px;")
        help_label.setWordWrap(True)
        group_layout.addRow(help_label)
        
        layout.addRow(group)
        layout.addStretch()
        
        return widget
    
    def _create_wechat_work_tab(self) -> QWidget:
        """创建企业微信配置页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        # 基础配置
        group1 = QGroupBox("基础配置")
        group1_layout = QFormLayout(group1)
        
        self.work_corp_id = QLineEdit()
        self.work_corp_id.setPlaceholderText("wwxxxxxx")
        group1_layout.addRow("企业ID:", self.work_corp_id)
        
        self.work_agent_id = QLineEdit()
        self.work_agent_id.setPlaceholderText("1000001")
        group1_layout.addRow("应用ID:", self.work_agent_id)
        
        self.work_corp_secret = QLineEdit()
        self.work_corp_secret.setPlaceholderText("输入应用的Secret")
        self.work_corp_secret.setEchoMode(QLineEdit.Password)
        group1_layout.addRow("应用Secret:", self.work_corp_secret)
        
        layout.addRow(group1)
        
        # 客户联系配置
        group2 = QGroupBox("客户联系配置（给外部客户发消息需要）")
        group2_layout = QFormLayout(group2)
        
        self.work_external_secret = QLineEdit()
        self.work_external_secret.setPlaceholderText("输入客户联系Secret")
        self.work_external_secret.setEchoMode(QLineEdit.Password)
        group2_layout.addRow("客户联系Secret:", self.work_external_secret)
        
        help_label = QLabel("💡 提示：在企业微信管理后台 -> 客户联系 -> API中获取")
        help_label.setStyleSheet("color: #666; font-size: 12px;")
        group2_layout.addRow(help_label)
        
        layout.addRow(group2)
        layout.addStretch()
        
        return widget
    
    def _create_wechat_mp_tab(self) -> QWidget:
        """创建公众号配置页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        group = QGroupBox("公众号配置")
        group_layout = QFormLayout(group)
        
        self.mp_app_id = QLineEdit()
        self.mp_app_id.setPlaceholderText("wxxxxxxx")
        group_layout.addRow("App ID:", self.mp_app_id)
        
        self.mp_app_secret = QLineEdit()
        self.mp_app_secret.setPlaceholderText("输入App Secret")
        self.mp_app_secret.setEchoMode(QLineEdit.Password)
        group_layout.addRow("App Secret:", self.mp_app_secret)
        
        help_label = QLabel("💡 提示：在微信公众平台 -> 开发 -> 基本配置中获取")
        help_label.setStyleSheet("color: #666; font-size: 12px;")
        help_label.setWordWrap(True)
        group_layout.addRow(help_label)
        
        layout.addRow(group)
        layout.addStretch()
        
        return widget
    
    def _create_ai_tab(self) -> QWidget:
        """创建AI配置页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        # OpenAI配置
        group1 = QGroupBox("OpenAI配置")
        group1_layout = QFormLayout(group1)
        
        self.ai_openai_key = QLineEdit()
        self.ai_openai_key.setPlaceholderText("sk-xxxxxxxx")
        self.ai_openai_key.setEchoMode(QLineEdit.Password)
        group1_layout.addRow("API Key:", self.ai_openai_key)
        
        self.ai_openai_url = QLineEdit()
        self.ai_openai_url.setPlaceholderText("https://api.openai.com/v1")
        group1_layout.addRow("Base URL:", self.ai_openai_url)
        
        layout.addRow(group1)
        
        # Anthropic配置
        group2 = QGroupBox("Anthropic (Claude) 配置")
        group2_layout = QFormLayout(group2)
        
        self.ai_anthropic_key = QLineEdit()
        self.ai_anthropic_key.setPlaceholderText("sk-ant-xxx")
        self.ai_anthropic_key.setEchoMode(QLineEdit.Password)
        group2_layout.addRow("API Key:", self.ai_anthropic_key)
        
        layout.addRow(group2)
        
        # 通义千问配置
        group3 = QGroupBox("阿里云通义千问配置")
        group3_layout = QFormLayout(group3)
        
        self.ai_dashscope_key = QLineEdit()
        self.ai_dashscope_key.setPlaceholderText("sk-xxxxxxxx")
        self.ai_dashscope_key.setEchoMode(QLineEdit.Password)
        group3_layout.addRow("API Key:", self.ai_dashscope_key)
        
        help_label = QLabel("💡 提示：在阿里云 -> 灵积模型服务 -> API-KEY中获取")
        help_label.setStyleSheet("color: #666; font-size: 12px;")
        group3_layout.addRow(help_label)
        
        layout.addRow(group3)
        layout.addStretch()
        
        return widget
    
    def _create_general_tab(self) -> QWidget:
        """创建通用配置页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        # 路径配置
        group1 = QGroupBox("路径配置")
        group1_layout = QFormLayout(group1)
        
        flow_dir_layout = QHBoxLayout()
        self.general_flow_dir = QLineEdit()
        self.general_flow_dir.setPlaceholderText("选择流程文件保存目录")
        flow_dir_layout.addWidget(self.general_flow_dir)
        
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self._browse_flow_dir)
        flow_dir_layout.addWidget(browse_btn)
        group1_layout.addRow("流程目录:", flow_dir_layout)
        
        layout.addRow(group1)
        
        # 外观配置
        group2 = QGroupBox("外观配置")
        group2_layout = QFormLayout(group2)
        
        self.general_theme = QComboBox()
        self.general_theme.addItems(["浅色", "深色", "自动"])
        group2_layout.addRow("主题:", self.general_theme)
        
        self.general_lang = QComboBox()
        self.general_lang.addItems(["简体中文", "English"])
        group2_layout.addRow("语言:", self.general_lang)
        
        layout.addRow(group2)
        layout.addStretch()
        
        return widget
    
    def _browse_flow_dir(self):
        """浏览流程目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择流程保存目录")
        if dir_path:
            self.general_flow_dir.setText(dir_path)
    
    def _load_config(self):
        """加载配置到界面"""
        # 飞书
        self.feishu_app_id.setText(self.config.get('feishu', 'app_id', ''))
        self.feishu_app_secret.setText(self.config.get('feishu', 'app_secret', ''))
        
        # 企业微信
        self.work_corp_id.setText(self.config.get('wechat_work', 'corp_id', ''))
        self.work_agent_id.setText(str(self.config.get('wechat_work', 'agent_id', '')))
        self.work_corp_secret.setText(self.config.get('wechat_work', 'corp_secret', ''))
        self.work_external_secret.setText(self.config.get('wechat_work', 'external_contact_secret', ''))
        
        # 公众号
        self.mp_app_id.setText(self.config.get('wechat_mp', 'app_id', ''))
        self.mp_app_secret.setText(self.config.get('wechat_mp', 'app_secret', ''))
        
        # AI
        self.ai_openai_key.setText(self.config.get('ai', 'openai_api_key', ''))
        self.ai_openai_url.setText(self.config.get('ai', 'openai_base_url', ''))
        self.ai_anthropic_key.setText(self.config.get('ai', 'anthropic_api_key', ''))
        self.ai_dashscope_key.setText(self.config.get('ai', 'dashscope_api_key', ''))
        
        # 通用
        self.general_flow_dir.setText(self.config.get('general', 'default_flow_dir', ''))
    
    def _save_config(self):
        """保存配置"""
        # 飞书
        self.config.set('feishu', 'app_id', self.feishu_app_id.text())
        self.config.set('feishu', 'app_secret', self.feishu_app_secret.text())
        
        # 企业微信
        self.config.set('wechat_work', 'corp_id', self.work_corp_id.text())
        self.config.set('wechat_work', 'agent_id', self.work_agent_id.text())
        self.config.set('wechat_work', 'corp_secret', self.work_corp_id.text())
        self.config.set('wechat_work', 'external_contact_secret', self.work_external_secret.text())
        
        # 公众号
        self.config.set('wechat_mp', 'app_id', self.mp_app_id.text())
        self.config.set('wechat_mp', 'app_secret', self.mp_app_secret.text())
        
        # AI
        self.config.set('ai', 'openai_api_key', self.ai_openai_key.text())
        self.config.set('ai', 'openai_base_url', self.ai_openai_url.text())
        self.config.set('ai', 'anthropic_api_key', self.ai_anthropic_key.text())
        self.config.set('ai', 'dashscope_api_key', self.ai_dashscope_key.text())
        
        # 通用
        self.config.set('general', 'default_flow_dir', self.general_flow_dir.text())
        
        # 保存到文件
        if self.config.save_config():
            QMessageBox.information(self, "保存成功", "配置已保存！")
        else:
            QMessageBox.warning(self, "保存失败", "配置保存失败，请检查权限")
    
    def _test_connection(self):
        """测试连接"""
        current_tab = self.tab_widget.currentIndex()
        tab_name = self.tab_widget.tabText(current_tab)
        
        QMessageBox.information(self, "测试连接", f"正在测试{tab_name}连接...\n\n（此功能开发中，请先保存配置后使用）")
    
    def _reset_config(self):
        """重置配置"""
        reply = QMessageBox.question(
            self, "确认重置",
            "确定要重置所有配置为默认值吗？此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.config.reset_to_default()
            self._load_config()
            QMessageBox.information(self, "重置成功", "配置已重置为默认值")
