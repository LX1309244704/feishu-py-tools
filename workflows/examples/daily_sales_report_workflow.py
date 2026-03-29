"""
示例工作流 - 每日销售报告生成
"""
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List


def main():
    """
    主函数（用于测试）
    """
    
    workflow = {
        "id": "daily_sales_report",
        "name": "每日销售报告生成",
        "description": "每天定时生成销售报告",
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "triggers": [
            {
                "id": "daily_trigger",
                "type": "schedule",
                "schedule": "0 9 * *",  # 每天9点
                "description": "每天9点触发"
            }
        ],
        "steps": [
            {
                "id": "step1",
                "name": "获取销售数据",
                "type": "api_call",
                "name": "get_sales_data",
                "config": {
                    "api_endpoint": "/api/bitable/records",
                    "method": "GET",
                    "params": {
                        "app_token": "AXDyb30BNamJJ6sMYh2cda7Gnxg",
                        "table_id": "tblcpk0OtPpxNwrs"
                    }
                }
            },
            {
                "id": "step2",
                "name": "处理数据",
                "type": "data_processing",
                "operation": "filter",
                "params": {
                    "field": "状态",
                    "value": "已售出"
                }
            },
            {
                "id": "step3",
                "name": "计算销售额",
                "type": "data_processing",
                "operation": "aggregate",
                "params": {
                    "field": "金额",
                    "function": "sum"
                }
            },
            {
                "id": "step4",
                "name": "生成报告",
                "type": "doc",
                "config": {
                    "api_endpoint": "/api/doc/documents",
                    "method": "POST",
                    "params": {
                        "title": f"每日销售报告-{datetime.now().strftime('%Y%m%d')}",
                        "content": f"""
# 每日销售报告 - {datetime.now().strftime('%Y年%m月%d')}

## 销售额总计：xxx
- 产品销量：xxx
- 新增客户：xxx
- 市场分析：xxx
"""
                    }
                }
            }
        ]
    }
    
    return workflow


if __name__ == '__main__':
    print("每日销售报告工作流:")
    print(json.dumps(workflow, indent=2))


# 导出工作流
def export_workflow(workflow, filename="daily_sales_report.json"):
    """导出工作流"""
    file_path = f"/workspace/projects/workspace/feishu-py-tools/workflows/examples/{filename}"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, ensure_ascii=False, indent=2)
    print(f"工作流已导出到: {file_path}")
    return file_path


if __name__ == '__main__':
    export_workflow(main())
