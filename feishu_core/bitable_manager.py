"""
飞书多维表格增强模块
"""
import requests
import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class BitableManager:
    """多维表格管理器"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        初始化多维表格管理器
        
        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self.tenant_access_token = None
    
    def _get_access_token(self) -> str:
        """获取租户访问令牌"""
        if self.tenant_access_token:
            return self.tenant_access_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if result.get("code") == 0:
            self.tenant_access_token = result.get("tenant_access_token")
            return self.tenant_access_token
        else:
            raise Exception(f"获取访问令牌失败: {result.get('msg')}")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }
    
    def list_tables(self, app_token: str) -> List[Dict[str, Any]]:
        """
        列出多维表格的所有数据表
        
        Args:
            app_token: 多维表格的 app_token
            
        Returns:
            数据表列表
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("items", [])
        else:
            raise Exception(f"获取数据表失败: {result.get('msg')}")
    
    def list_records(self, app_token: str, table_id: str, 
                     page_size: int = 100, page_token: str = None) -> Dict[str, Any]:
        """
        列出数据表记录
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            page_size: 每页记录数
            page_token: 分页令牌
            
        Returns:
            记录列表
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        params = {
            "page_size": page_size
        }
        
        if page_token:
            params["page_token"] = page_token
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取记录失败: {result.get('msg')}")
    
    def create_record(self, app_token: str, table_id: str, 
                     fields: Dict[str, Any]) -> str:
        """
        创建一条记录
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            fields: 记录字段数据
            
        Returns:
            记录ID
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        data = {"fields": fields}
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("record", {}).get("record_id")
        else:
            raise Exception(f"创建记录失败: {result.get('msg')}")
    
    def batch_create_records(self, app_token: str, table_id: str,
                            records: List[Dict[str, Any]]) -> List[str]:
        """
        批量创建记录
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            records: 记录列表
            
        Returns:
            记录ID列表
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
        data = {"records": [{"fields": r} for r in records]}
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return [r.get("record_id") for r in result.get("data", {}).get("records", [])]
        else:
            raise Exception(f"批量创建记录失败: {result.get('msg')}")
    
    def update_record(self, app_token: str, table_id: str, 
                     record_id: str, fields: Dict[str, Any]) -> bool:
        """
        更新记录
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            record_id: 记录ID
            fields: 更新的字段数据
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        data = {"fields": fields}
        
        response = requests.put(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        return result.get("code") == 0
    
    def delete_record(self, app_token: str, table_id: str, record_id: str) -> bool:
        """
        删除记录
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            record_id: 记录ID
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        response = requests.delete(url, headers=self._get_headers())
        result = response.json()
        
        return result.get("code") == 0
    
    def get_record(self, app_token: str, table_id: str, record_id: str) -> Dict[str, Any]:
        """
        获取单条记录
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            record_id: 记录ID
            
        Returns:
            记录数据
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("record", {})
        else:
            raise Exception(f"获取记录失败: {result.get('msg')}")
    
    def search_records(self, app_token: str, table_id: str, 
                     filter_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        搜索记录
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            filter_dict: 筛选条件
            
        Returns:
            记录列表
        """
        # 先获取所有记录，然后在客户端过滤
        all_records = self.list_records(app_token, table_id)
        filtered_records = []
        
        for record in all_records.get("items", []):
            match = True
            for key, value in filter_dict.items():
                if key not in record.get("fields", {}):
                    match = False
                    break
                if record["fields"][key] != value:
                    match = False
                    break
            
            if match:
                filtered_records.append(record)
        
        return filtered_records
    
    def export_to_csv(self, app_token: str, table_id: str, 
                     output_file: str = None) -> str:
        """
        导出数据到CSV
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            output_file: 输出文件路径
            
        Returns:
            CSV内容或文件路径
        """
        import csv
        import io
        
        # 获取所有记录
        all_records = self.list_records(app_token, table_id)
        records = all_records.get("items", [])
        
        if not records:
            return ""
        
        # 获取所有字段名
        field_names = list(records[0].get("fields", {}).keys())
        
        # 创建CSV内容
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=field_names)
        writer.writeheader()
        
        for record in records:
            writer.writerow(record.get("fields", {}))
        
        csv_content = output.getvalue()
        
        # 如果指定了输出文件，保存到文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8-sig') as f:
                f.write(csv_content)
            return output_file
        
        return csv_content
    
    def import_from_csv(self, app_token: str, table_id: str, 
                      csv_file: str) -> int:
        """
        从CSV导入数据
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            csv_file: CSV文件路径
            
        Returns:
            导入的记录数
        """
        import csv
        
        records = []
        
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
        
        if records:
            record_ids = self.batch_create_records(app_token, table_id, records)
            return len(record_ids)
        
        return 0
    
    def get_table_info(self, app_token: str, table_id: str) -> Dict[str, Any]:
        """
        获取数据表信息
        
        Args:
            app_token: 多维表格的 app_token
            table_id: 数据表的 table_id
            
        Returns:
            数据表信息
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取数据表信息失败: {result.get('msg')}")
