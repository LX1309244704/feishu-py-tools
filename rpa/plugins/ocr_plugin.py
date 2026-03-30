"""
OCR插件
基于PaddleOCR实现，支持图片、截图、PDF中的文字识别
"""
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import os
import numpy as np
from typing import Dict, Any, List, Optional
import json

from rpa.core.plugin import BasePlugin, register_plugin


@register_plugin
class OCRPlugin(BasePlugin):
    """OCR文字识别插件"""
    plugin_name = "ai/ocr"
    plugin_version = "1.0.0"
    plugin_description = "OCR文字识别插件，支持图片、截图、PDF中的文字提取"
    plugin_author = "三金的小虾米"
    
    # 全局OCR实例，懒加载
    _ocr_instance = None
    
    @classmethod
    def get_ocr(cls, lang: str = 'ch', use_gpu: bool = False, **kwargs):
        """获取OCR实例"""
        if cls._ocr_instance is None:
            cls._ocr_instance = PaddleOCR(
                use_angle_cls=True,
                lang=lang,
                use_gpu=use_gpu,
                show_log=False,
                **kwargs
            )
        return cls._ocr_instance
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行OCR识别
        
        Args:
            params:
                action: 操作类型
                    - recognize: 识别图片文字
                    - recognize_and_draw: 识别并绘制结果
                    - batch_recognize: 批量识别
                image_path: 图片路径（recognize/recognize_and_draw时必填）
                image_paths: 图片路径列表（batch_recognize时必填）
                lang: 语言，默认ch（中英文），可选en/chinese_cht等
                use_gpu: 是否使用GPU，默认False
                output_path: 结果输出路径（recognize_and_draw时必填）
                return_detail: 是否返回详细位置信息，默认False
        """
        action = params.get('action', 'recognize')
        lang = params.get('lang', 'ch')
        use_gpu = params.get('use_gpu', False)
        return_detail = params.get('return_detail', False)
        
        try:
            # 获取OCR实例
            ocr = self.get_ocr(lang=lang, use_gpu=use_gpu)
            
            if action == 'recognize':
                image_path = params.get('image_path')
                if not image_path or not os.path.exists(image_path):
                    return {'success': False, 'error': 'image_path不存在'}
                
                # 执行识别
                result = ocr.ocr(image_path, cls=True)
                
                # 处理结果
                full_text = []
                details = []
                
                for idx in range(len(result)):
                    res = result[idx]
                    for line in res:
                        box = line[0]  # 四个点坐标
                        text = line[1][0]  # 识别文字
                        confidence = line[1][1]  # 置信度
                        
                        full_text.append(text)
                        details.append({
                            'text': text,
                            'confidence': float(confidence),
                            'box': [list(map(int, point)) for point in box]
                        })
                
                return {
                    'success': True,
                    'full_text': '\n'.join(full_text),
                    'text_lines': full_text,
                    'details': details if return_detail else None,
                    'line_count': len(full_text)
                }
            
            elif action == 'recognize_and_draw':
                image_path = params.get('image_path')
                output_path = params.get('output_path', 'ocr_result.jpg')
                if not image_path or not os.path.exists(image_path):
                    return {'success': False, 'error': 'image_path不存在'}
                
                # 识别
                result = ocr.ocr(image_path, cls=True)
                result = result[0]
                
                # 绘制结果
                image = Image.open(image_path).convert('RGB')
                boxes = [line[0] for line in result]
                txts = [line[1][0] for line in result]
                scores = [line[1][1] for line in result]
                
                # 生成图片
                im_show = draw_ocr(image, boxes, txts, scores, font_path='doc/fonts/simfang.ttf')
                im_show = Image.fromarray(im_show)
                im_show.save(output_path)
                
                # 提取文本
                full_text = '\n'.join(txts)
                
                return {
                    'success': True,
                    'full_text': full_text,
                    'text_lines': txts,
                    'output_path': output_path,
                    'count': len(txts)
                }
            
            elif action == 'batch_recognize':
                image_paths = params.get('image_paths', [])
                if not image_paths or not isinstance(image_paths, list):
                    return {'success': False, 'error': 'image_paths应为数组'}
                
                results = []
                all_text = []
                
                for path in image_paths:
                    if not os.path.exists(path):
                        results.append({'path': path, 'success': False, 'error': '文件不存在'})
                        continue
                    
                    try:
                        res = ocr.ocr(path, cls=True)
                        txts = [line[1][0] for line in res[0]]
                        full_text = '\n'.join(txts)
                        results.append({
                            'path': path,
                            'success': True,
                            'full_text': full_text,
                            'line_count': len(txts)
                        })
                        all_text.append(full_text)
                    except Exception as e:
                        results.append({'path': path, 'success': False, 'error': str(e)})
                
                return {
                    'success': True,
                    'results': results,
                    'total_count': len(results),
                    'success_count': sum(1 for r in results if r['success']),
                    'all_text': '\n\n'.join(all_text)
                }
            
            else:
                return {'success': False, 'error': f'不支持的action: {action}'}
        
        except Exception as e:
            return {'success': False, 'error': f'OCR识别失败: {str(e)}'}
