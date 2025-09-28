#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证记账应用是否正常工作
"""

import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """测试导入是否正常"""
    try:
        import streamlit as st
        print("✅ Streamlit 导入成功")
    except ImportError as e:
        print(f"❌ Streamlit 导入失败: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas 导入成功")
    except ImportError as e:
        print(f"❌ Pandas 导入失败: {e}")
        return False
    
    try:
        import openpyxl
        print("✅ OpenPyXL 导入成功")
    except ImportError as e:
        print(f"❌ OpenPyXL 导入失败: {e}")
        return False
    
    try:
        import plotly
        print("✅ Plotly 导入成功")
    except ImportError as e:
        print(f"❌ Plotly 导入失败: {e}")
        return False
    
    return True

def test_data_manager():
    """测试数据管理器"""
    try:
        from data_manager import DataManager
        print("✅ DataManager 导入成功")
        
        # 创建测试数据管理器
        dm = DataManager(data_dir="test_data", filename="test_records.xlsx")
        print("✅ DataManager 初始化成功")
        
        # 测试添加记录
        from datetime import datetime
        success = dm.add_record(
            record_type="支出",
            amount=100.50,
            category="餐饮",
            date=datetime.now(),
            note="测试记录"
        )
        
        if success:
            print("✅ 添加记录测试成功")
        else:
            print("❌ 添加记录测试失败")
            return False
        
        # 测试获取记录
        records = dm.get_all_records()
        if not records.empty:
            print("✅ 获取记录测试成功")
        else:
            print("❌ 获取记录测试失败")
            return False
        
        # 清理测试数据
        import shutil
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
            print("✅ 测试数据清理完成")
        
        return True
        
    except Exception as e:
        print(f"❌ DataManager 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 我的记账本 - 测试脚本")
    print("=" * 50)
    
    # 测试导入
    print("\n📦 测试依赖包导入...")
    if not test_imports():
        print("\n❌ 依赖包测试失败，请先安装依赖：pip install -r requirements.txt")
        return False
    
    # 测试数据管理器
    print("\n🗄️ 测试数据管理器...")
    if not test_data_manager():
        print("\n❌ 数据管理器测试失败")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 所有测试通过！应用可以正常运行")
    print("=" * 50)
    print("\n🚀 启动应用：")
    print("   Windows: 双击 start.bat")
    print("   Linux/Mac: ./start.sh")
    print("   或直接运行: streamlit run app.py")
    print("\n📱 应用地址: http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
