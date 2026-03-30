#!/usr/bin/env python3
"""
启动RPA客户端
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from rpa.gui.main import main
    main()
