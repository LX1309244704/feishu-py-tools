"""
流程管理页面
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QTextEdit, QPushButton,
    QFileDialog, QMessageBox, QDialog, QFormLayout,
    QLineEdit, QDialogButtonBox, QTabWidget
)
from PySide6.QtGui import QFont, QIcon, QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import Qt, QRegularExpression

from rpa.core.flow import load_flow, Flow
from rpa.core.engine import execution_engine
import yaml
import json
from pathlib import Path


class YAMLSyntaxHighlighter(QSyntaxHighlighter):
    """YAML语法高亮"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_rules()
    
    def _init_rules(self):
        self.highlighting_rules = []
        
        # 键名
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#d73a49"))
        key_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append(
            (QRegularExpression(r"^[a-zA-Z0-9_]+:"), key_format)
        )
        
        # 字符串
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#032f62"))
        self.highlighting_rules.append(
            (QRegularExpression(r"\".*\""), string_format)
        )
        self.highlighting_rules.append(
            (QRegularExpression(r"'.*'"), string_format)
        )
        
        # 数字
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#005cc5"))
        self.highlighting_rules.append(
            (QRegularExpression(r"\b\d+\.?\d*\b"), number_format)
        )
        
        # 布尔值
        bool_format = QTextCharFormat()
        bool_format.setForeground(QColor("#6f42c1"))
        self.highlighting_rules.append(
            (QRegularExpression(r"\b(true|false|null)\b"), bool_format)
        )
        
        # 注释
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6a737d"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append(
            (QRegularExpression(r"#.*$"), comment_format)
        )
        
        # 变量${{ }}
        var_format = QTextCharFormat()
        var_format.setForeground(QColor("#22863a"))
        var_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append(
            (QRegularExpression(r"\$\{\{[^}]*\}\}"), var_format)
        )
    
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


class FlowPage(QWidget):
    """流程管理页面"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self._init_ui()
    
    def _init_ui(self):
        """初始化界面"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 左侧：流程列表
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        left_title = QLabel("<h3>流程列表</h3>")
        left_layout.addWidget(left_title)
        
        self.flow_list = QListWidget()
        self.flow_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)
        self.flow_list.itemDoubleClicked.connect(self._on_flow_selected)
        left_layout.addWidget(self.flow_list)
        
        # 左侧按钮
        btn_layout = QHBoxLayout()
        add_btn = QPushButton(QIcon(":/icons/new.png"), "新建")
        add_btn.clicked.connect(self.new_flow)
        open_btn = QPushButton(QIcon(":/icons/open.png"), "打开")
        open_btn.clicked.connect(self._open_flow_dialog)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(open_btn)
        left_layout.addLayout(btn_layout)
        
        # 右侧：编辑器和操作区
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 顶部工具栏
        toolbar_layout = QHBoxLayout()
        
        self.save_btn = QPushButton(QIcon(":/icons/save.png"), "保存")
        self.save_btn.clicked.connect(self.save_flow)
        self.save_as_btn = QPushButton("另存为")
        self.save_as_btn.clicked.connect(self.save_flow_as)
        self.run_btn = QPushButton(QIcon(":/icons/run.png"), "执行")
        self.run_btn.clicked.connect(self.run_flow)
        self.validate_btn = QPushButton("验证")
        self.validate_btn.clicked.connect(lambda: self.validate_flow(show_msg=True))
        toolbar_layout.addWidget(self.save_btn)
        toolbar_layout.addWidget(self.save_as_btn)
        toolbar_layout.addWidget(self.run_btn)
        toolbar_layout.addWidget(self.validate_btn)
        toolbar_layout.addStretch()
        
        right_layout.addLayout(toolbar_layout)
        
        # 编辑器
        self.tab_widget = QTabWidget()
        
        # YAML编辑器
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 12))
        self.highlighter = YAMLSyntaxHighlighter(self.editor.document())
        self.editor.setTabStopDistance(20)
        self.editor.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
                line-height: 1.5;
            }
        """)
        self.tab_widget.addTab(self.editor, "YAML编辑")
        
        # 日志输出
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                background-color: #f8f9fa;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
        """)
        self.tab_widget.addTab(self.log_output, "执行日志")
        
        right_layout.addWidget(self.tab_widget)
        
        # 分割窗口
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 3)  # 右侧占3/4宽度
        
        main_layout.addWidget(splitter)
        
        # 加载本地流程
        self._load_local_flows()
    
    def _load_local_flows(self):
        """加载本地流程文件"""
        self.flow_list.clear()
        # 加载当前目录下的yaml文件
        current_dir = Path(".")
        yaml_files = list(current_dir.glob("*.yaml")) + list(current_dir.glob("*.yml")) + list(current_dir.glob("*.json"))
        
        for f in yaml_files[:10]:  # 最多显示10个
            item = QListWidgetItem(f.name)
            item.setData(Qt.UserRole, str(f.absolute()))
            self.flow_list.addItem(item)
    
    def _on_flow_selected(self, item):
        """选择流程"""
        file_path = item.data(Qt.UserRole)
        self.open_flow(file_path)
    
    def _open_flow_dialog(self):
        """打开流程对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开流程文件", "",
            "流程文件 (*.yaml *.yml *.json);;所有文件 (*.*)"
        )
        if file_path:
            self.open_flow(file_path)
    
    def new_flow(self):
        """新建流程"""
        # 弹出对话框输入流程名称
        dialog = QDialog(self)
        dialog.setWindowTitle("新建流程")
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout(dialog)
        name_input = QLineEdit()
        name_input.setPlaceholderText("输入流程名称，比如：库存预警流程")
        desc_input = QLineEdit()
        desc_input.setPlaceholderText("输入流程描述（可选）")
        
        layout.addRow("流程名称：", name_input)
        layout.addRow("流程描述：", desc_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec() == QDialog.Accepted:
            name = name_input.text().strip()
            if not name:
                QMessageBox.warning(self, "警告", "流程名称不能为空")
                return
            
            # 生成默认流程内容
            desc = desc_input.text().strip()
            default_content = f"""# RPA流程定义
name: {name}
description: "{desc}"
version: 1.0.0

trigger:
  type: manual

variables:
  app_id: "cli_xxxxxx"
  app_secret: "xxxxxx"

steps:
  - name: 示例步骤
    uses: feishu/bitable@1.0.0
    with:
      action: list_tables
      app_token: "xxxxxx"
      app_id: "${{ globals.app_id }}"
      app_secret: "${{ globals.app_secret }}"
"""
            self.editor.setPlainText(default_content)
            self.current_file = None
            self._append_log(f"新建流程：{name}")
    
    def open_flow(self, file_path):
        """打开流程文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.editor.setPlainText(content)
            self.current_file = file_path
            self._append_log(f"打开流程：{file_path}")
            
            # 添加到列表
            if not self.flow_list.findItems(Path(file_path).name, Qt.MatchExactly):
                item = QListWidgetItem(Path(file_path).name)
                item.setData(Qt.UserRole, file_path)
                self.flow_list.addItem(item)
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开文件失败：{str(e)}")
    
    def save_flow(self):
        """保存流程"""
        if not self.current_file:
            return self.save_flow_as()
        
        try:
            content = self.editor.toPlainText()
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)
            self._append_log(f"流程已保存：{self.current_file}")
            return True
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败：{str(e)}")
            return False
    
    def save_flow_as(self):
        """另存为"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存流程文件", "",
            "YAML文件 (*.yaml *.yml);;JSON文件 (*.json);;所有文件 (*.*)"
        )
        if file_path:
            self.current_file = file_path
            return self.save_flow()
        return False
    
    def validate_flow(self, show_msg=False):
        """验证流程格式"""
        content = self.editor.toPlainText()
        if not content:
            if show_msg:
                QMessageBox.warning(self, "警告", "流程内容为空")
            return False, "内容为空"
        
        try:
            # 先尝试解析为YAML/JSON
            if self.current_file and self.current_file.endswith('.json'):
                data = json.loads(content)
            else:
                data = yaml.safe_load(content)
            
            # 验证Flow
            flow = Flow(data)
            if show_msg:
                QMessageBox.information(self, "验证成功", "流程格式正确！")
            self._append_log("流程验证成功")
            return True, "验证成功"
            
        except Exception as e:
            error_msg = f"格式错误：{str(e)}"
            if show_msg:
                QMessageBox.warning(self, "验证失败", error_msg)
            self._append_log(f"流程验证失败：{error_msg}")
            return False, error_msg
    
    def run_flow(self):
        """执行流程"""
        # 先验证
        valid, msg = self.validate_flow()
        if not valid:
            QMessageBox.warning(self, "验证失败", msg)
            return
        
        try:
            # 保存临时文件
            temp_file = Path("temp_flow.yaml")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            
            # 加载流程
            flow = load_flow(str(temp_file))
            self._append_log(f"开始执行流程：{flow.name} v{flow.version}")
            
            # 执行流程
            result = execution_engine.execute_flow(flow)
            
            # 输出结果
            if result['status'] == 'success':
                self._append_log(f"✅ 流程执行成功！耗时：{result['duration']:.2f}秒")
                for step in result['steps']:
                    status = "✅" if step['status'] == 'success' else "❌"
                    self._append_log(f"  {status} {step['name']} - {step['duration']:.2f}s")
            else:
                self._append_log(f"❌ 流程执行失败：{result.get('error', '未知错误')}")
            
            # 切换到日志页
            self.tab_widget.setCurrentIndex(1)
            
            # 删除临时文件
            temp_file.unlink(missing_ok=True)
            
        except Exception as e:
            self._append_log(f"❌ 执行异常：{str(e)}")
            self.tab_widget.setCurrentIndex(1)
    
    def debug_flow(self):
        """调试流程"""
        self._append_log("调试功能开发中...")
        QMessageBox.information(self, "调试", "调试功能正在开发中...")
    
    def _append_log(self, message):
        """添加日志"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{time_str}] {message}\n"
        self.log_output.append(log_msg)
        # 滚动到底部
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
