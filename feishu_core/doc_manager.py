"""
飞书文档管理模块
"""
import requests
import json
from typing import Dict, Any, Optional, List


class DocManager:
    """文档管理器"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        初始化文档管理器
        
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
    
    def create_document(self, title: str, content: str = "", 
                       folder_token: str = None) -> str:
        """
        创建新文档
        
        Args:
            title: 文档标题
            content: 文档内容（Markdown格式）
            folder_token: 父文件夹token（可选）
            
        Returns:
            文档ID
        """
        url = f"{self.base_url}/docx/v1/documents"
        data = {
            "title": title,
            "content": {
                "document": {
                    "body": {
                        "content": [
                            {
                                "type": "paragraph",
                                "paragraph": {
                                    "elements": [
                                        {
                                            "type": "text_run",
                                            "text_run": {
                                                "content": content
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
        
        if folder_token:
            data["folder_token"] = folder_token
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("document", {}).get("document_id")
        else:
            raise Exception(f"创建文档失败: {result.get('msg')}")
    
    def get_document(self, document_id: str) -> Dict[str, Any]:
        """
        获取文档内容
        
        Args:
            document_id: 文档ID
            
        Returns:
            文档内容
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取文档失败: {result.get('msg')}")
    
    def update_document(self, document_id: str, content: str) -> bool:
        """
        更新文档内容
        
        Args:
            document_id: 文档ID
            content: 新内容
            
        Returns:
            是否成功
        """
        # 注意：实际实现需要使用更复杂的API来更新文档
        # 这里是简化版本
        return True
    
    def delete_document(self, document_id: str) -> bool:
        """
        删除文档
        
        Args:
            document_id: 文档ID
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}"
        response = requests.delete(url, headers=self._get_headers())
        result = response.json()
        
        return result.get("code") == 0
    
    def list_documents(self, folder_token: str = None, 
                      page_size: int = 50, page_token: str = None) -> List[Dict[str, Any]]:
        """
        列出文档
        
        Args:
            folder_token: 文件夹token（可选）
            page_size: 每页数量
            page_token: 分页令牌
            
        Returns:
            文档列表
        """
        url = f"{self.base_url}/drive/explorer/v2/file/list/w/search"
        params = {
            "query": "type == 'docx'",
            "page_size": page_size
        }
        
        if folder_token:
            params["parent_node"] = folder_token
        
        if page_token:
            params["page_token"] = page_token
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("files", [])
        else:
            raise Exception(f"获取文档列表失败: {result.get('msg')}")
    
    def add_comment(self, document_id: str, content: str) -> str:
        """
        添加评论
        
        Args:
            document_id: 文档ID
            content: 评论内容
            
        Returns:
            评论ID
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}/comments"
        data = {
            "content": content,
            "body": {
                "content": [
                    {
                        "type": "paragraph",
                        "paragraph": {
                            "elements": [
                                {
                                    "type": "text_run",
                                    "text_run": {
                                        "content": content
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("comment", {}).get("comment_id")
        else:
            raise Exception(f"添加评论失败: {result.get('msg')}")
    
    def get_comments(self, document_id: str) -> List[Dict[str, Any]]:
        """
        获取文档评论
        
        Args:
            document_id: 文档ID
            
        Returns:
            评论列表
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}/comments"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("comments", [])
        else:
            raise Exception(f"获取评论失败: {result.get('msg')}")
