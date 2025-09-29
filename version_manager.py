#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本管理脚本
用于管理应用版本号、更新日志和发布流程
"""

import os
import re
import datetime
from typing import Dict, List, Tuple

class VersionManager:
    def __init__(self):
        self.app_file = "app.py"
        self.version_file = "VERSION.md"
        self.changelog_file = "CHANGELOG.md"
        self.readme_file = "README.md"
        
    def get_current_version(self) -> str:
        """获取当前版本号"""
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'APP_VERSION = "([^"]+)"', content)
                if match:
                    return match.group(1)
        except Exception as e:
            print(f"读取版本号失败: {e}")
        return "1.0.0"
    
    def get_current_build_date(self) -> str:
        """获取当前构建日期"""
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'APP_BUILD_DATE = "([^"]+)"', content)
                if match:
                    return match.group(1)
        except Exception as e:
            print(f"读取构建日期失败: {e}")
        return datetime.date.today().strftime("%Y-%m-%d")
    
    def parse_version(self, version: str) -> Tuple[int, int, int]:
        """解析版本号"""
        try:
            parts = version.split('.')
            major = int(parts[0]) if len(parts) > 0 else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
            return major, minor, patch
        except:
            return 1, 0, 0
    
    def increment_version(self, version: str, increment_type: str) -> str:
        """增加版本号"""
        major, minor, patch = self.parse_version(version)
        
        if increment_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif increment_type == "minor":
            minor += 1
            patch = 0
        elif increment_type == "patch":
            patch += 1
        else:
            raise ValueError("increment_type 必须是 'major', 'minor' 或 'patch'")
        
        return f"{major}.{minor}.{patch}"
    
    def update_app_version(self, new_version: str, build_date: str = None):
        """更新app.py中的版本信息"""
        if build_date is None:
            build_date = datetime.date.today().strftime("%Y-%m-%d")
        
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新版本号
            content = re.sub(
                r'APP_VERSION = "[^"]+"',
                f'APP_VERSION = "{new_version}"',
                content
            )
            
            # 更新构建日期
            content = re.sub(
                r'APP_BUILD_DATE = "[^"]+"',
                f'APP_BUILD_DATE = "{build_date}"',
                content
            )
            
            with open(self.app_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新 {self.app_file} 中的版本信息")
            print(f"   版本号: {new_version}")
            print(f"   构建日期: {build_date}")
            
        except Exception as e:
            print(f"❌ 更新 {self.app_file} 失败: {e}")
    
    def add_changelog_entry(self, version: str, changes: Dict[str, List[str]], build_date: str = None):
        """添加更新日志条目"""
        if build_date is None:
            build_date = datetime.date.today().strftime("%Y-%m-%d")
        
        try:
            with open(self.changelog_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 构建新的更新日志条目
            entry = f"\n## [{version}] - {build_date}\n\n"
            
            for change_type, items in changes.items():
                if items:
                    entry += f"### {change_type}\n"
                    for item in items:
                        entry += f"- {item}\n"
                    entry += "\n"
            
            # 在"未发布"部分后插入新条目
            if "## [未发布]" in content:
                content = content.replace("## [未发布]", f"## [未发布]\n{entry}")
            else:
                content = entry + content
            
            with open(self.changelog_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已添加更新日志条目: v{version}")
            
        except Exception as e:
            print(f"❌ 添加更新日志失败: {e}")
    
    def update_version_file(self, version: str, build_date: str = None):
        """更新版本清单文件"""
        if build_date is None:
            build_date = datetime.date.today().strftime("%Y-%m-%d")
        
        try:
            with open(self.version_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新当前版本
            content = re.sub(
                r'\*\*v[\d.]+\*\* - .*',
                f'**v{version}** - 最新版本 ({build_date})',
                content
            )
            
            with open(self.version_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新 {self.version_file}")
            
        except Exception as e:
            print(f"❌ 更新 {self.version_file} 失败: {e}")
    
    def create_release_notes(self, version: str, changes: Dict[str, List[str]]) -> str:
        """创建发布说明"""
        notes = f"# {version} 发布说明\n\n"
        notes += f"**发布日期**: {datetime.date.today().strftime('%Y年%m月%d日')}\n\n"
        
        for change_type, items in changes.items():
            if items:
                notes += f"## {change_type}\n"
                for item in items:
                    notes += f"- {item}\n"
                notes += "\n"
        
        return notes
    
    def show_current_info(self):
        """显示当前版本信息"""
        version = self.get_current_version()
        build_date = self.get_current_build_date()
        major, minor, patch = self.parse_version(version)
        
        print("📋 当前版本信息")
        print("=" * 40)
        print(f"版本号: v{version}")
        print(f"主版本: {major}")
        print(f"次版本: {minor}")
        print(f"修订版: {patch}")
        print(f"构建日期: {build_date}")
        print(f"版本类型: ", end="")
        
        if patch > 0:
            print("修订版本 (Bug修复)")
        elif minor > 0:
            print("次版本 (新功能)")
        else:
            print("主版本 (重大更新)")
    
    def interactive_update(self):
        """交互式版本更新"""
        current_version = self.get_current_version()
        print(f"当前版本: v{current_version}")
        print("\n请选择更新类型:")
        print("1. 修订版本 (patch) - Bug修复")
        print("2. 次版本 (minor) - 新功能")
        print("3. 主版本 (major) - 重大更新")
        print("4. 自定义版本号")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            new_version = self.increment_version(current_version, "patch")
        elif choice == "2":
            new_version = self.increment_version(current_version, "minor")
        elif choice == "3":
            new_version = self.increment_version(current_version, "major")
        elif choice == "4":
            new_version = input("请输入新版本号 (格式: x.y.z): ").strip()
        else:
            print("❌ 无效选择")
            return
        
        print(f"\n新版本号: v{new_version}")
        confirm = input("确认更新? (y/N): ").strip().lower()
        
        if confirm == 'y':
            self.update_app_version(new_version)
            self.update_version_file(new_version)
            print(f"\n✅ 版本已更新到 v{new_version}")
            print("💡 请手动更新 CHANGELOG.md 文件")
        else:
            print("❌ 更新已取消")

def main():
    """主函数"""
    manager = VersionManager()
    
    print("🚀 版本管理工具")
    print("=" * 40)
    
    while True:
        print("\n请选择操作:")
        print("1. 查看当前版本信息")
        print("2. 交互式版本更新")
        print("3. 退出")
        
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == "1":
            manager.show_current_info()
        elif choice == "2":
            manager.interactive_update()
        elif choice == "3":
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()
