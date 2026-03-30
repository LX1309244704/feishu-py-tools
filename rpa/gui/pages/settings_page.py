"""
设置页面 - 使用配置对话框
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGroupBox, QFormLayout, QTextEdit
)
from PySide6.QtCore import Qt

from ..utils.config_dialog import ConfigDialog
from ..utils.config_manager import get_config


class SettingsPage(QWidget):
    """设置页面"""
    
    def __init__(self):
        super().__init__()
        self.config = get_config()
        self._init_ui()
    
    def _init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 标题
        title = QLabel("<h2>⚙️ 系统设置</h2>")
        main_layout.addWidget(title)
        
        # 快速配置按钮区域
        config_group = QGroupBox("快速配置")
        config_layout = QVBoxLayout(config_group)
        
        config_hint = QLabel("点击下方按钮打开配置管理器，配置所有平台参数：")
        config_hint.setStyleSheet("color: #666;")
        config_layout.addWidget(config_hint)
        
        # 打开配置按钮
        self.open_config_btn = QPushButton("🔧 打开配置管理器")
        self.open_config_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.open_config_btn.clicked.connect(self._open_config_dialog)
        config_layout.addWidget(self.open_config_btn)
        
        # 配置状态概览
        status_label = QLabel("当前配置状态：")
        status_label.setStyleSheet("margin-top: 10px; font-weight: bold;")
        config_layout.addWidget(status_label)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        self.status_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                background-color: #f8f9fa;
            }
        """)
        config_layout.addWidget(self.status_text)
        
        main_layout.addWidget(config_group)
        
        # 项目信息
        info_group = QGroupBox("关于微元Weiyuan")
        info_layout = QFormLayout(info_group)
        
        info_layout.addRow("版本:", QLabel("2.0.0"))
        info_layout.addRow("开发团队:", QLabel("三金的小虾米"))
        info_layout.addRow("邮箱:", QLabel("1309244704@qq.com"))
        
        github_link = QLabel("<a href='https://github.com/LX1309244704/weiyuan'>GitHub仓库</a>")
        github_link.setOpenExternalLinks(True)
        info_layout.addRow("项目主页:", github_link)
        
        main_layout.addWidget(info_group)
        
        # 功能列表
        features_group = QGroupBox("已集成功能")
        features_layout = QVBoxLayout(features_group)
        
        features_text = """
        ✅ 飞书生态：多维表格、消息、文档
        ✅ 微信全生态：个人微信、企业微信、公众号
        ✅ 内容平台：小红书、抖音、视频号自动发布
        ✅ UI自动化：桌面操作、浏览器自动化
        ✅ AI增强：OCR识别、大模型集成
        ✅ 多种使用方式：CLI、PC客户端、Web控制台
        """
        features_label = QLabel(features_text)
        features_label.setStyleSheet("line-height: 1.8;")
        features_layout.addWidget(features_label)
        
        main_layout.addWidget(features_group)
        
        main_layout.addStretch()
        
        # 加载配置状态
        self._load_config_status()
    
    def _open_config_dialog(self):
        """打开配置对话框"""
        dialog = ConfigDialog(self)
        dialog.exec()
        # 对话框关闭后刷新状态
        self._load_config_status()
    
    def _load_config_status(self):
        """加载配置状态"""
        status = []
        
        # 飞书
        feishu_app_id = self.config.get('feishu', 'app_id', '')
        status.append(f"飞书配置：{'✅ 已配置' if feishu_app_id else '❌ 未配置'}")
        
        # 企业微信
        work_corp_id = self.config.get('wechat_work', 'corp_id', '')
        status.append(f"企业微信配置：{'✅ 已配置' if work_corp_id else '❌ 未配置'}")
        
        # 公众号
        mp_app_id = self.config.get('wechat_mp', 'app_id', '')
        status.append(f"公众号配置：{'✅ 已配置' if mp_app_id else '❌ 未配置'}")
        
        # AI
        ai_configured = any([
            self.config.get('ai', 'openai_api_key', ''),
            self.config.get('ai', 'anthropic_api_key', ''),
            self.config.get('ai', 'dashscope_api_key', '')
        ])
        status.append(f"AI配置：{'✅ 已配置' if ai_configured else '❌ 未配置'}")
        
        self.status_text.setText('\n'.join(status))
