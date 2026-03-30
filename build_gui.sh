#!/bin/bash
# PyInstaller打包脚本，生成PC客户端
# 支持Windows/macOS/Linux

APP_NAME="RPA工具"
VERSION="1.0.0"

echo "开始打包 $APP_NAME v$VERSION ..."

# 安装依赖
pip install pyinstaller
pip install -r requirements.txt
pip install -r requirements_rpa.txt
pip install -r requirements_gui.txt

# 打包
pyinstaller --onefile \
            --windowed \
            --name "$APP_NAME" \
            --icon rpa/gui/resources/app.ico \
            --add-data "rpa/schemas/*:rpa/schemas" \
            --add-data "rpa/templates/*:rpa/templates" \
            --add-data "rpa/gui/resources/*:rpa/gui/resources" \
            start_gui.py

echo "打包完成！输出文件在 dist/ 目录下"
