"""
RPA工具PC客户端主入口
基于PySide6开发
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QStatusBar, QMenuBar, QMenu, QSplitter,
    QToolBar, QMessageBox, QFileDialog
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QSize, QSettings

# 导入页面
from .pages.dashboard_page import DashboardPage
from .pages.flow_page import FlowPage
from .pages.execution_page import ExecutionPage
from .pages.template_page import TemplatePage
from .pages.plugin_page import PluginPage
from .pages.settings_page import SettingsPage


class RPAMainWindow(QMainWindow):
    """RPA工具主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPA机器人流程自动化工具")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)
        
        # 全局设置
        self.settings = QSettings("FeishuTools", "RPA Client")
        
        # 初始化UI
        self._init_ui()
        self._init_menu()
        self._init_toolbar()
        self._init_statusbar()
        
        # 加载窗口状态
        self._load_settings()
    
    def _init_ui(self):
        """初始化主界面"""
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setIconSize(QSize(24, 24))
        
        # 添加页面
        self.dashboard_page = DashboardPage()
        self.flow_page = FlowPage()
        self.execution_page = ExecutionPage()
        self.template_page = TemplatePage()
        self.plugin_page = PluginPage()
        self.settings_page = SettingsPage()
        
        self.tab_widget.addTab(self.dashboard_page, QIcon(":/icons/dashboard.png"), "首页")
        self.tab_widget.addTab(self.flow_page, QIcon(":/icons/flow.png"), "流程管理")
        self.tab_widget.addTab(self.execution_page, QIcon(":/icons/history.png"), "执行记录")
        self.tab_widget.addTab(self.template_page, QIcon(":/icons/template.png"), "模板市场")
        self.tab_widget.addTab(self.plugin_page, QIcon(":/icons/plugin.png"), "插件中心")
        self.tab_widget.addTab(self.settings_page, QIcon(":/icons/settings.png"), "设置")
        
        main_layout.addWidget(self.tab_widget)
        
        # 标签页切换信号
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
    
    def _init_menu(self):
        """初始化菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        new_flow_action = QAction(QIcon(":/icons/new.png"), "新建流程", self)
        new_flow_action.setShortcut("Ctrl+N")
        new_flow_action.triggered.connect(self._new_flow)
        file_menu.addAction(new_flow_action)
        
        open_flow_action = QAction(QIcon(":/icons/open.png"), "打开流程", self)
        open_flow_action.setShortcut("Ctrl+O")
        open_flow_action.triggered.connect(self._open_flow)
        file_menu.addAction(open_flow_action)
        
        file_menu.addSeparator()
        
        save_action = QAction(QIcon(":/icons/save.png"), "保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_current)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("另存为", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self._save_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 执行菜单
        run_menu = menubar.addMenu("执行")
        
        run_action = QAction(QIcon(":/icons/run.png"), "执行当前流程", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self._run_current_flow)
        run_menu.addAction(run_action)
        
        stop_action = QAction(QIcon(":/icons/stop.png"), "停止执行", self)
        stop_action.setShortcut("Shift+F5")
        stop_action.triggered.connect(self._stop_execution)
        run_menu.addAction(stop_action)
        
        run_menu.addSeparator()
        
        debug_action = QAction(QIcon(":/icons/debug.png"), "调试执行", self)
        debug_action.setShortcut("F6")
        debug_action.triggered.connect(self._debug_flow)
        run_menu.addAction(debug_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu("工具")
        
        validate_action = QAction("验证当前流程", self)
        validate_action.triggered.connect(self._validate_flow)
        tools_menu.addAction(validate_action)
        
        import_template_action = QAction("导入模板", self)
        import_template_action.triggered.connect(self._import_template)
        tools_menu.addAction(import_template_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        docs_action = QAction("使用文档", self)
        docs_action.triggered.connect(self._open_docs)
        help_menu.addAction(docs_action)
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _init_toolbar(self):
        """初始化工具栏"""
        toolbar = QToolBar("主工具栏")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # 工具栏按钮
        toolbar.addAction(QIcon(":/icons/new.png"), "新建流程", self._new_flow)
        toolbar.addAction(QIcon(":/icons/open.png"), "打开流程", self._open_flow)
        toolbar.addAction(QIcon(":/icons/save.png"), "保存", self._save_current)
        toolbar.addSeparator()
        toolbar.addAction(QIcon(":/icons/run.png"), "执行", self._run_current_flow)
        toolbar.addAction(QIcon(":/icons/stop.png"), "停止", self._stop_execution)
        toolbar.addSeparator()
        toolbar.addAction(QIcon(":/icons/settings.png"), "设置", lambda: self.tab_widget.setCurrentIndex(5))
    
    def _init_statusbar(self):
        """初始化状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
    
    def _load_settings(self):
        """加载窗口设置"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 保存窗口状态
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
        # 确认退出
        reply = QMessageBox.question(
            self, "确认退出", "确定要退出RPA工具吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    # 菜单动作函数
    def _on_tab_changed(self, index):
        """标签页切换"""
        self.status_bar.showMessage(f"切换到 {self.tab_widget.tabText(index)} 页面")
    
    def _new_flow(self):
        """新建流程"""
        self.tab_widget.setCurrentIndex(1)
        self.flow_page.new_flow()
        self.status_bar.showMessage("新建流程")
    
    def _open_flow(self):
        """打开流程"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开流程文件", "",
            "流程文件 (*.yaml *.yml *.json);;所有文件 (*.*)"
        )
        if file_path:
            self.tab_widget.setCurrentIndex(1)
            self.flow_page.open_flow(file_path)
            self.status_bar.showMessage(f"打开流程: {os.path.basename(file_path)}")
    
    def _save_current(self):
        """保存当前流程"""
        if self.tab_widget.currentIndex() == 1:
            saved = self.flow_page.save_flow()
            if saved:
                self.status_bar.showMessage("流程已保存")
            else:
                self.status_bar.showMessage("保存失败")
        else:
            self.status_bar.showMessage("当前页面无需保存")
    
    def _save_as(self):
        """另存为"""
        if self.tab_widget.currentIndex() == 1:
            saved = self.flow_page.save_flow_as()
            if saved:
                self.status_bar.showMessage("流程已另存为")
            else:
                self.status_bar.showMessage("保存失败")
    
    def _run_current_flow(self):
        """执行当前流程"""
        if self.tab_widget.currentIndex() == 1:
            self.flow_page.run_flow()
            self.status_bar.showMessage("开始执行流程")
    
    def _stop_execution(self):
        """停止执行"""
        # 后续实现
        self.status_bar.showMessage("已停止执行")
    
    def _debug_flow(self):
        """调试流程"""
        if self.tab_widget.currentIndex() == 1:
            self.flow_page.debug_flow()
            self.status_bar.showMessage("开始调试流程")
    
    def _validate_flow(self):
        """验证流程"""
        if self.tab_widget.currentIndex() == 1:
            valid, msg = self.flow_page.validate_flow()
            if valid:
                QMessageBox.information(self, "验证成功", "流程格式正确！")
                self.status_bar.showMessage("流程验证成功")
            else:
                QMessageBox.warning(self, "验证失败", f"流程格式错误：{msg}")
                self.status_bar.showMessage("流程验证失败")
    
    def _import_template(self):
        """导入模板"""
        self.tab_widget.setCurrentIndex(3)
        self.status_bar.showMessage("切换到模板市场")
    
    def _open_docs(self):
        """打开文档"""
        # 后续实现
        QMessageBox.information(self, "文档", "使用文档正在开发中...")
    
    def _show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, "关于RPA工具",
            "<h3>RPA机器人流程自动化工具</h3>"
            "<p>版本：1.0.0</p>"
            "<p>基于飞书Python工具箱开发</p>"
            "<p>© 2026 三金的小虾米</p>"
            "<p><a href='https://github.com/LX1309244704/feishu-py-tools'>GitHub仓库</a></p>"
        )


def main():
    """启动客户端"""
    # 高DPI适配
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    app.setApplicationName("RPA工具")
    app.setOrganizationName("FeishuTools")
    app.setWindowIcon(QIcon(":/icons/app.png"))
    
    window = RPAMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
