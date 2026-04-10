#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装依赖脚本

使用方法:
    python install.py
"""

import subprocess
import sys


def install_packages():
    """安装所需的 Python 包"""
    packages = [
        'flask>=2.0.0',
        'werkzeug>=2.0.0',
        'python-docx>=0.8.11',
        'Pillow>=9.0.0',
    ]
    
    print("=" * 50)
    print("📦 安装依赖")
    print("=" * 50)
    
    for package in packages:
        print(f"\n安装 {package}...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package
            ])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 所有依赖安装完成！")
    print("=" * 50)
    return True


if __name__ == '__main__':
    success = install_packages()
    if success:
        print("\n🚀 现在可以运行: python app.py")
