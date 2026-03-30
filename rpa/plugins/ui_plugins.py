"""
UI自动化插件
支持桌面UI操作和浏览器自动化
"""
import pyautogui
import time
import os
from typing import Dict, Any, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from rpa.core.plugin import BasePlugin, register_plugin

# 配置pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


@register_plugin
class DesktopAutoPlugin(BasePlugin):
    """桌面UI自动化插件"""
    plugin_name = "ui/desktop"
    plugin_version = "1.0.0"
    plugin_description = "桌面UI自动化插件，支持鼠标、键盘、窗口操作、图像识别"
    plugin_author = "三金的小虾米"
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行桌面自动化操作
        
        Args:
            params:
                action: 操作类型
                    - mouse_click: 鼠标点击
                    - mouse_move: 鼠标移动
                    - mouse_scroll: 鼠标滚动
                    - key_press: 按键
                    - type_text: 输入文本
                    - hotkey: 快捷键
                    - screenshot: 截图
                    - locate_image: 图像识别定位
                    - wait_image: 等待图片出现
                    - get_position: 获取鼠标位置
        """
        action = params.get('action')
        if not action:
            return {'success': False, 'error': '缺少action参数'}
        
        try:
            if action == 'mouse_click':
                x = params.get('x')
                y = params.get('y')
                button = params.get('button', 'left')
                clicks = params.get('clicks', 1)
                interval = params.get('interval', 0.25)
                
                if x is not None and y is not None:
                    pyautogui.click(x=x, y=y, button=button, clicks=clicks, interval=interval)
                else:
                    pyautogui.click(button=button, clicks=clicks, interval=interval)
                return {'success': True, 'result': f'鼠标点击成功: ({x}, {y})' if x else '鼠标点击成功'}
            
            elif action == 'mouse_move':
                x = params.get('x')
                y = params.get('y')
                duration = params.get('duration', 0.2)
                pyautogui.moveTo(x, y, duration=duration)
                return {'success': True, 'result': f'鼠标移动到: ({x}, {y})'}
            
            elif action == 'mouse_scroll':
                clicks = params.get('clicks', 1)
                x = params.get('x')
                y = params.get('y')
                if x and y:
                    pyautogui.scroll(clicks, x=x, y=y)
                else:
                    pyautogui.scroll(clicks)
                return {'success': True, 'result': f'鼠标滚动: {clicks}格'}
            
            elif action == 'key_press':
                key = params.get('key')
                presses = params.get('presses', 1)
                interval = params.get('interval', 0.2)
                if not key:
                    return {'success': False, 'error': '缺少key参数'}
                pyautogui.press(key, presses=presses, interval=interval)
                return {'success': True, 'result': f'按键: {key} 共{presses}次'}
            
            elif action == 'type_text':
                text = params.get('text')
                interval = params.get('interval', 0.05)
                if not text:
                    return {'success': False, 'error': '缺少text参数'}
                pyautogui.typewrite(text, interval=interval)
                return {'success': True, 'result': f'输入文本: {text}'}
            
            elif action == 'hotkey':
                keys = params.get('keys', [])
                if not keys or not isinstance(keys, list):
                    return {'success': False, 'error': 'keys参数应为数组'}
                pyautogui.hotkey(*keys)
                return {'success': True, 'result': f'快捷键: {"+".join(keys)}'}
            
            elif action == 'screenshot':
                save_path = params.get('save_path', 'screenshot.png')
                region = params.get('region')  # (left, top, width, height)
                if region:
                    img = pyautogui.screenshot(region=region)
                else:
                    img = pyautogui.screenshot()
                img.save(save_path)
                return {'success': True, 'result': f'截图已保存: {save_path}', 'path': save_path}
            
            elif action == 'locate_image':
                image_path = params.get('image_path')
                confidence = params.get('confidence', 0.8)
                grayscale = params.get('grayscale', False)
                if not image_path or not os.path.exists(image_path):
                    return {'success': False, 'error': 'image_path不存在'}
                
                location = pyautogui.locateOnScreen(image_path, confidence=confidence, grayscale=grayscale)
                if location:
                    center = pyautogui.center(location)
                    return {
                        'success': True, 
                        'result': '找到图片',
                        'position': {'x': center.x, 'y': center.y},
                        'box': {'left': location.left, 'top': location.top, 'width': location.width, 'height': location.height}
                    }
                else:
                    return {'success': False, 'error': '未找到图片'}
            
            elif action == 'wait_image':
                image_path = params.get('image_path')
                timeout = params.get('timeout', 10)
                confidence = params.get('confidence', 0.8)
                if not image_path or not os.path.exists(image_path):
                    return {'success': False, 'error': 'image_path不存在'}
                
                start_time = time.time()
                while time.time() - start_time < timeout:
                    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                    if location:
                        center = pyautogui.center(location)
                        return {
                            'success': True,
                            'result': '图片出现',
                            'position': {'x': center.x, 'y': center.y},
                            'wait_time': time.time() - start_time
                        }
                    time.sleep(0.5)
                return {'success': False, 'error': f'等待超时{timeout}秒，图片未出现'}
            
            elif action == 'get_position':
                x, y = pyautogui.position()
                return {'success': True, 'position': {'x': x, 'y': y}}
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
        
        except Exception as e:
            return {'success': False, 'error': f'操作失败: {str(e)}'}


@register_plugin
class BrowserAutoPlugin(BasePlugin):
    """浏览器自动化插件"""
    plugin_name = "ui/browser"
    plugin_version = "1.0.0"
    plugin_description = "浏览器自动化插件，支持Chrome操作、元素定位、网页交互"
    plugin_author = "三金的小虾米"
    
    _driver = None  # 全局浏览器实例
    
    @classmethod
    def get_driver(cls, headless: bool = False, options: Optional[Dict] = None):
        """获取浏览器驱动"""
        if cls._driver:
            return cls._driver
        
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless=new")
        
        # 自定义选项
        if options:
            if 'arguments' in options and isinstance(options['arguments'], list):
                for arg in options['arguments']:
                    chrome_options.add_argument(arg)
        
        # 启动浏览器
        cls._driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        cls._driver.implicitly_wait(10)
        return cls._driver
    
    @classmethod
    def close_driver(cls):
        """关闭浏览器"""
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行浏览器自动化操作
        
        Args:
            params:
                action: 操作类型
                    - open: 打开网页
                    - close: 关闭浏览器
                    - find_element: 查找元素
                    - click: 点击元素
                    - input: 输入文本
                    - get_text: 获取元素文本
                    - get_attribute: 获取元素属性
                    - wait_element: 等待元素出现
                    - execute_script: 执行JS
                    - screenshot: 页面截图
                    - switch_tab: 切换标签页
                    - back: 后退
                    - forward: 前进
                    - refresh: 刷新
        """
        action = params.get('action')
        if not action:
            return {'success': False, 'error': '缺少action参数'}
        
        # 不需要driver的操作
        if action == 'close':
            self.close_driver()
            return {'success': True, 'result': '浏览器已关闭'}
        
        try:
            # 获取driver
            headless = params.get('headless', False)
            driver_options = params.get('options', {})
            driver = self.get_driver(headless=headless, options=driver_options)
            
            if action == 'open':
                url = params.get('url')
                if not url:
                    return {'success': False, 'error': '缺少url参数'}
                driver.get(url)
                return {'success': True, 'result': f'打开页面: {url}', 'title': driver.title}
            
            elif action == 'find_element':
                by = params.get('by', 'css')  # css/xpath/id/class/name/tag/link_text/partial_link_text
                value = params.get('value')
                if not value:
                    return {'success': False, 'error': '缺少value参数'}
                
                by_map = {
                    'css': By.CSS_SELECTOR,
                    'xpath': By.XPATH,
                    'id': By.ID,
                    'class': By.CLASS_NAME,
                    'name': By.NAME,
                    'tag': By.TAG_NAME,
                    'link_text': By.LINK_TEXT,
                    'partial_link_text': By.PARTIAL_LINK_TEXT
                }
                if by not in by_map:
                    return {'success': False, 'error': f'不支持的定位方式: {by}'}
                
                elements = driver.find_elements(by_map[by], value)
                return {
                    'success': True, 
                    'count': len(elements),
                    'elements': [{'text': e.text, 'tag_name': e.tag_name} for e in elements]
                }
            
            elif action == 'click':
                by = params.get('by', 'css')
                value = params.get('value')
                if not value:
                    return {'success': False, 'error': '缺少value参数'}
                
                by_map = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'id': By.ID}
                element = driver.find_element(by_map.get(by, By.CSS_SELECTOR), value)
                element.click()
                return {'success': True, 'result': '点击元素成功'}
            
            elif action == 'input':
                by = params.get('by', 'css')
                value = params.get('value')
                text = params.get('text')
                clear_before = params.get('clear_before', True)
                if not value or text is None:
                    return {'success': False, 'error': '缺少value或text参数'}
                
                by_map = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'id': By.ID}
                element = driver.find_element(by_map.get(by, By.CSS_SELECTOR), value)
                if clear_before:
                    element.clear()
                element.send_keys(text)
                return {'success': True, 'result': f'输入文本: {text}'}
            
            elif action == 'get_text':
                by = params.get('by', 'css')
                value = params.get('value')
                if not value:
                    return {'success': False, 'error': '缺少value参数'}
                
                by_map = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'id': By.ID}
                element = driver.find_element(by_map.get(by, By.CSS_SELECTOR), value)
                return {'success': True, 'text': element.text}
            
            elif action == 'execute_script':
                script = params.get('script')
                args = params.get('args', [])
                if not script:
                    return {'success': False, 'error': '缺少script参数'}
                result = driver.execute_script(script, *args)
                return {'success': True, 'result': result}
            
            elif action == 'wait_element':
                by = params.get('by', 'css')
                value = params.get('value')
                timeout = params.get('timeout', 10)
                condition = params.get('condition', 'presence')  # presence/visible/clickable
                if not value:
                    return {'success': False, 'error': '缺少value参数'}
                
                by_map = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'id': By.ID}
                locator = (by_map.get(by, By.CSS_SELECTOR), value)
                
                if condition == 'presence':
                    EC_cond = EC.presence_of_element_located(locator)
                elif condition == 'visible':
                    EC_cond = EC.visibility_of_element_located(locator)
                elif condition == 'clickable':
                    EC_cond = EC.element_to_be_clickable(locator)
                else:
                    return {'success': False, 'error': f'不支持的条件: {condition}'}
                
                element = WebDriverWait(driver, timeout).until(EC_cond)
                return {'success': True, 'result': '元素已出现'}
            
            elif action == 'screenshot':
                save_path = params.get('save_path', 'browser_screenshot.png')
                driver.save_screenshot(save_path)
                return {'success': True, 'result': f'页面截图已保存: {save_path}'}
            
            elif action == 'switch_tab':
                index = params.get('index', 0)
                driver.switch_to.window(driver.window_handles[index])
                return {'success': True, 'result': f'切换到标签页{index}'}
            
            elif action == 'back':
                driver.back()
                return {'success': True, 'result': '页面后退'}
            
            elif action == 'forward':
                driver.forward()
                return {'success': True, 'result': '页面前进'}
            
            elif action == 'refresh':
                driver.refresh()
                return {'success': True, 'result': '页面刷新'}
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
        
        except Exception as e:
            return {'success': False, 'error': f'浏览器操作失败: {str(e)}'}
