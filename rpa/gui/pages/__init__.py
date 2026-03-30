"""
GUI页面模块
"""
from .dashboard_page import DashboardPage
from .flow_page import FlowPage
from .execution_page import ExecutionPage
from .template_page import TemplatePage
from .plugin_page import PluginPage
from .settings_page import SettingsPage

__all__ = [
    'DashboardPage',
    'FlowPage',
    'ExecutionPage',
    'TemplatePage',
    'PluginPage',
    'SettingsPage',
]
