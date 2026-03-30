"""
Weiyuan - 飞书Python工具箱
安装脚本
"""
from setuptools import setup, find_packages
import os

# 读取README
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_file, 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取requirements
requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(requirements_file, 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='weiyuan',
    version='1.0.0',
    author='三金的小虾米',
    author_email='1309244704@qq.com',
    description='基于飞书CLI的Python增强版飞书管理工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/LX1309244704/weiyuan',
    project_urls={
        'Bug Reports': 'https://github.com/LX1309244704/weiyuan/issues',
        'Source': 'https://github.com/LX1309244704/weiyuan',
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'feishu-cli=feishu_cli.main:main',
            'feishu-server=feishu_cli.server:main',
        ],
    },
    keywords=[
        'feishu',
        'lark',
        '飞书',
        'bitable',
        '多维表格',
        'automation',
        'workflow',
        'ai',
        'cli',
    ],
    include_package_data=True,
    package_data={
        'feishu_cli': ['config/*.yaml'],
        'templates': ['base/*.json', 'doc/*.json', 'workflow/*.json'],
    },
)
