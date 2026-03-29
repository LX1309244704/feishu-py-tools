"""
示例插件 - 发送库存预警通知
"""
import requests
from typing import Dict, Any, List, Optional
from plugins.plugin_system import Plugin


class InventoryAlertPlugin(Plugin):
    """库存预警插件"""
    
    def __init__(self):
        """
        初始化插件
        """
        super().__init__(
            plugin_id="inventory_alert",
            name="库存预警",
            version="1.0.0",
            description="当商品库存低于最小库存时发送通知",
            author="三金的小虾米"
        )
        
        # 配置
        self.config = {
            "min_stock_alert": True,
            "alert_method": "message",
            "recipient": "",
            "app_id": "",
            "app_secret": "",
            "table_id": "",
            "min_stock_column": "最小库存",
            "current_stock_column": "当前库存",
            "product_name_column": "商品名称"
        }
        
        self.hooks = {
            "before_send": "before_send_alert",
            "after_send": "after_send_alert"
        }
        
        # 依赖
        self.dependencies = [
            "pandas>=2.0.0"
        ]
        
        self.metadata = {
            "icon": "📦",
            "type": "workflow",
            "category": "notification",
            "tags": ["库存", "预警", "通知", "自动化"],
            "conditions": [
                "min_stock_alert",
                "inventory_management"
            ]
        }
    
    def get_config_schema(self) -> Dict[str, Any]:
        """获取配置schema"""
        return {
            "type": "object",
            "properties": {
                "min_stock_alert": {
                    "type": "boolean",
                    "description": "是否启用库存预警",
                    "default": True
                },
                "alert_method": {
                    "type": "string",
                    "description": "预警方式",
                    "enum": ["message", "email"],
                    "default": "message"
                },
                "recipient": {
                    "type": "string",
                    "description": "接收人ID"
                },
                "app_id": {
                    "type": "string",
                    "description": "飞书应用ID"
                },
                "app_secret": {
                    "type": "string",
                    "description": "飞书应用密钥"
                },
                "table_id": {
                    "type": "string",
                    "description": "数据表ID"
                },
                "min_stock_column": {
                    "type": "string",
                    "description": "最小库存字段名"
                },
                "current_stock_column": {
                    "type": "string",
                    "description": "当前库存字段名"
                },
                "product_name_column": {
                    "type": "string",
                    "description": "商品名称字段名"
                },
                "warning_threshold": {
                    "type": "integer",
                    "description": "预警阈值（默认为0，即低于等于也警告）",
                    "default": 0
                }
            },
            "required": ["min_stock_alert", "min_stock_column", "current_stock_column", "product_name_column"]
        }
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, any]:
        """
        执行库存预警检查
        """
        try:
            min_stock_column = self.config.get("min_stock_column", "")
            current_stock_column = self.config.get("current_stock_column", "")
            product_name_column = self.config.get("product_name_column", "")
            warning_threshold = self.config.get("warning_threshold", 0)

            # 获取数据
            data = context.get("data", [])
            if not data:
                return {"success": False, "error": "未提供数据"}

            low_stock_items = []
            for item in data:
                min_stock = item.get(min_stock_column, 0)
                current_stock = item.get(current_stock_column, 0)
                product_name = item.get(product_name_column, "未知商品")

                if current_stock <= min_stock:
                    low_stock_items.append(item)

            if low_stock_items:
                message = f"库存预警：{len(low_stock_items)}个商品库存不足："
                for item in low_stock_items:
                    message += f"\n- {item.get(product_name_column)}：{item.get(current_stock_column)}/{item.get(min_stock_column)}"

                # 发送通知
                recipient = self.config.get("recipient", "")
                if recipient:
                    self._send_notification(item.get(product_name_column, "未知商品"), item, recipient)

                # 记录日志
                print(f"已发送预警：{message}")

                # 标记已处理
                for item in low_stock_items:
                    self._mark_as_processed(item, "预警已发送")

                return {
                    "success": True,
                    "low_stock_items": low_stock_items,
                    "alert_count": len(low_stock_items),
                    "message": message
                }

            return {
                "success": True,
                "low_stock_items": [],
                "alert_count": 0,
                "message": "所有商品库存正常"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"库存预警失败: {str(e)}"
            }
    
    def _send_notification(self, product_name: str, item: Dict[str, Any], recipient: str):
        """发送通知"""
        from feishu_core.message_manager import MessageManager

        manager = MessageManager(
            app_id=self.config.get("app_id", ""),
            app_secret=self.config.get("app_secret", "")
        )

        message = f"【库存预警】商品「{product_name}」库存不足，请及时补货！"

        try:
            msg_id = manager.send_text_message(
                receive_id=recipient,
                content=message,
                receive_id_type="open_id"
            )
            print(f"预警消息已发送，消息ID: {msg_id}")
        except Exception as e:
            print(f"发送通知失败: {e}")
    
    def _mark_as_processed(self, item: Dict[str, Any], note: str):
        """标记已处理"""
        if "_processing_logs" not in item:
            item["_processing_logs"] = []
        item["_processing_logs"].append({
            "time": datetime.now().isoformat(),
            "note": note,
            "status": "alerted"
        })
        self._save_plugin_file()
    
    def get_info(self) -> Dict[str, Any]:
        """获取插件信息"""
        return {
            "plugin_id": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "config": self.config,
            "hooks": list(self.hooks.keys()),
            "dependencies": self.dependencies,
            "enabled": self.enabled,
            "metadata": self.metadata
        }
    
    def before_send_alert(self, item: Dict[str, Any]):
        """发送前钩子"""
        print(f"即将发送预警: {item.get('商品名称')}")
    
    def after_send_alert(self, item: Dict[str, Any]):
        """发送后钩子"""
        print(f"预警已发送: {item.get('商品名称')}")


def main():
    """主函数（用于测试）"""
    plugin = InventoryAlertPlugin()
    print("插件信息：")
    print(plugin.get_info())


if __name__ == '__main__':
    main()
