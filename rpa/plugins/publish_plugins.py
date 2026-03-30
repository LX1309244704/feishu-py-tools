"""
内容平台发布插件
支持小红书、抖音、视频号自动上传内容
"""
import time
from typing import Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip

from rpa.core.plugin import BasePlugin, register_plugin


@register_plugin
class ContentPublishPlugin(BasePlugin):
    """内容平台自动发布插件"""
    plugin_name = "publish/content"
    plugin_version = "1.0.0"
    plugin_description = "内容平台自动发布插件，支持小红书、抖音、视频号"
    plugin_author = "三金的小虾米"
    
    def _wait_and_click(self, driver, by, value, timeout=10):
        """等待元素出现并点击"""
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return element
    
    def _wait_for_element(self, driver, by, value, timeout=10):
        """等待元素出现"""
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def _input_text(self, element, text):
        """输入文本，先清空再输入"""
        element.clear()
        # 用剪贴板粘贴的方式，避免输入法问题
        pyperclip.copy(text)
        element.send_keys(pyperclip.paste())
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        发布内容到内容平台
        
        Args:
            params:
                platform: 平台：xiaohongshu/抖音/douyin/视频号/wechat_channel
                title: 内容标题
                content: 内容正文/描述
                files: 媒体文件路径列表（图片/视频）
                tags: 标签列表，可选
                publish_time: 定时发布时间，可选，格式YYYY-MM-DD HH:MM
                category: 分类/领域，可选
                headless: 是否无头模式，默认False
                cookies_path: 保存的cookie路径，可选，免登录
        """
        platform = params.get('platform', '').lower()
        title = params.get('title', '')
        content = params.get('content', '')
        files = params.get('files', [])
        tags = params.get('tags', [])
        publish_time = params.get('publish_time')
        category = params.get('category')
        headless = params.get('headless', False)
        cookies_path = params.get('cookies_path')
        
        if not platform:
            return {'success': False, 'error': '请指定发布平台'}
        if not files or not isinstance(files, list) or len(files) == 0:
            return {'success': False, 'error': '请指定要上传的媒体文件'}
        for f in files:
            import os
            if not os.path.exists(f):
                return {'success': False, 'error': f'文件不存在：{f}'}
        
        try:
            # 导入浏览器插件
            from rpa.plugins.ui_plugins import BrowserAutoPlugin
            browser = BrowserAutoPlugin()
            
            # 启动浏览器
            driver = browser.get_driver(headless=headless, options={
                'arguments': [
                    '--start-maximized',
                    '--disable-notifications',
                    '--disable-popup-blocking',
                ]
            })
            
            # 加载cookies（如果有）
            if cookies_path and os.path.exists(cookies_path):
                import json
                with open(cookies_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            
            result = {}
            if platform in ['xiaohongshu', '小红书']:
                result = self._publish_xiaohongshu(driver, title, content, files, tags, publish_time)
            elif platform in ['douyin', '抖音']:
                result = self._publish_douyin(driver, title, content, files, tags, publish_time)
            elif platform in ['wechat_channel', '视频号']:
                result = self._publish_wechat_channel(driver, title, content, files, tags, publish_time)
            else:
                result = {'success': False, 'error': f'不支持的平台：{platform}'}
            
            # 保存cookies
            if cookies_path and result['success']:
                cookies = driver.get_cookies()
                with open(cookies_path, 'w', encoding='utf-8') as f:
                    import json
                    json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            # 关闭浏览器（可选，默认保留方便用户确认）
            # browser.close_driver()
            
            return result
        
        except Exception as e:
            return {'success': False, 'error': f'发布失败：{str(e)}'}
    
    def _publish_xiaohongshu(self, driver, title, content, files, tags, publish_time=None):
        """发布小红书笔记"""
        try:
            # 打开小红书创作者平台
            driver.get("https://creator.xiaohongshu.com/publish/publish")
            time.sleep(3)
            
            # 检查是否登录
            if "登录" in driver.title:
                return {'success': False, 'error': '请先扫码登录小红书，登录后重新执行'}
            
            # 上传图片/视频
            upload_input = self._wait_for_element(driver, By.CSS_SELECTOR, 'input[type="file"]')
            upload_input.send_keys('\n'.join(files))
            time.sleep(10)  # 等待上传完成
            
            # 输入标题
            title_input = self._wait_for_element(driver, By.CSS_SELECTOR, 'input[placeholder="填写标题会有更多赞哦～"]')
            self._input_text(title_input, title)
            
            # 输入正文
            content_editor = self._wait_for_element(driver, By.CSS_SELECTOR, 'div[contenteditable="true"]')
            self._input_text(content_editor, content)
            
            # 添加标签
            if tags and len(tags) > 0:
                # 点击添加话题按钮
                self._wait_and_click(driver, By.CSS_SELECTOR, '.topic-btn')
                time.sleep(1)
                for tag in tags:
                    tag_input = self._wait_for_element(driver, By.CSS_SELECTOR, '.topic-input input')
                    self._input_text(tag_input, tag)
                    time.sleep(2)
                    # 选择第一个标签
                    self._wait_and_click(driver, By.CSS_SELECTOR, '.dropdown-container .item:first-child')
                    time.sleep(1)
            
            # 设置定时发布
            if publish_time:
                # 点击定时发布
                self._wait_and_click(driver, By.XPATH, '//*[text()="定时发布"]')
                time.sleep(1)
                # 选择时间
                # 这里需要根据实际页面元素调整
                pass
            
            # 点击发布按钮
            self._wait_and_click(driver, By.XPATH, '//*[text()="发布"]')
            time.sleep(3)
            
            return {'success': True, 'platform': '小红书', 'message': '发布成功'}
        
        except Exception as e:
            return {'success': False, 'error': f'小红书发布失败：{str(e)}'}
    
    def _publish_douyin(self, driver, title, content, files, tags, publish_time=None):
        """发布抖音作品"""
        try:
            # 打开抖音创作者服务平台
            driver.get("https://creator.douyin.com/creator-micro/content/upload")
            time.sleep(3)
            
            if "登录" in driver.title:
                return {'success': False, 'error': '请先扫码登录抖音，登录后重新执行'}
            
            # 上传视频
            upload_input = self._wait_for_element(driver, By.CSS_SELECTOR, 'input[type="file"]')
            upload_input.send_keys(files[0])  # 抖音一次只能传一个视频
            time.sleep(15)  # 等待上传和转码
            
            # 输入标题和描述
            title_input = self._wait_for_element(driver, By.CSS_SELECTOR, '.public-DraftEditor-content')
            full_content = f"{title}\n{content}\n"
            if tags:
                full_content += ' '.join([f"#{tag}" for tag in tags])
            self._input_text(title_input, full_content)
            
            # 选择分类
            if category:
                # 选择分类
                pass
            
            # 定时发布
            if publish_time:
                # 开启定时发布
                self._wait_and_click(driver, By.XPATH, '//*[text()="定时发布"]')
                time.sleep(1)
                # 设置时间
                pass
            
            # 点击发布
            self._wait_and_click(driver, By.XPATH, '//*[text()="发布"]')
            time.sleep(3)
            
            return {'success': True, 'platform': '抖音', 'message': '发布成功'}
        
        except Exception as e:
            return {'success': False, 'error': f'抖音发布失败：{str(e)}'}
    
    def _publish_wechat_channel(self, driver, title, content, files, tags, publish_time=None):
        """发布视频号内容"""
        try:
            # 打开视频号助手
            driver.get("https://channels.weixin.qq.com/platform/post/create")
            time.sleep(3)
            
            if "登录" in driver.title:
                return {'success': False, 'error': '请先扫码登录视频号助手，登录后重新执行'}
            
            # 上传视频
            upload_input = self._wait_for_element(driver, By.CSS_SELECTOR, 'input[type="file"]')
            upload_input.send_keys(files[0])
            time.sleep(10)
            
            # 输入标题
            title_input = self._wait_for_element(driver, By.CSS_SELECTOR, 'input[placeholder="填写标题（选填）"]')
            if title:
                self._input_text(title_input, title)
            
            # 输入描述
            desc_input = self._wait_for_element(driver, By.CSS_SELECTOR, 'div[placeholder="添加描述（选填，@朋友、添加话题、位置会获得更多曝光）"]')
            full_content = content
            if tags:
                full_content += '\n' + ' '.join([f"#{tag}" for tag in tags])
            self._input_text(desc_input, full_content)
            
            # 定时发布
            if publish_time:
                # 选择定时发布
                self._wait_and_click(driver, By.XPATH, '//*[text()="定时发表"]')
                time.sleep(1)
                # 设置时间
                pass
            
            # 点击发表
            self._wait_and_click(driver, By.XPATH, '//*[text()="发表"]')
            time.sleep(3)
            
            return {'success': True, 'platform': '视频号', 'message': '发布成功'}
        
        except Exception as e:
            return {'success': False, 'error': f'视频号发布失败：{str(e)}'}
