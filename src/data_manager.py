import pandas as pd
import os
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

class DataManager:
    def __init__(self, data_dir="data", filename="account_records.xlsx"):
        """
        初始化数据管理器
        
        Args:
            data_dir (str): 数据存储目录
            filename (str): Excel文件名
        """
        self.data_dir = data_dir
        self.filename = filename
        self.file_path = os.path.join(data_dir, filename)
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
        
        # 初始化Excel文件
        self._init_excel_file()
    
    def _init_excel_file(self):
        """初始化Excel文件，如果不存在则创建"""
        if not os.path.exists(self.file_path):
            # 创建空的DataFrame
            df = pd.DataFrame(columns=[
                'ID', '类型', '金额', '分类', '日期', '备注', '创建时间'
            ])
            
            # 保存到Excel
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='记账记录', index=False)
                
                # 获取工作表并设置样式
                worksheet = writer.sheets['记账记录']
                self._format_excel_sheet(worksheet)
    
    def _format_excel_sheet(self, worksheet):
        """格式化Excel工作表"""
        # 设置标题行样式
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="2E86AB", end_color="2E86AB", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        # 设置边框
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # 应用标题行样式
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = thin_border
        
        # 设置列宽
        column_widths = {
            'A': 8,   # ID
            'B': 10,  # 类型
            'C': 12,  # 金额
            'D': 15,  # 分类
            'E': 20,  # 日期
            'F': 30,  # 备注
            'G': 20   # 创建时间
        }
        
        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width
        
        # 冻结首行
        worksheet.freeze_panes = 'A2'
    
    def add_record(self, record_type, amount, category, date, note=""):
        """
        添加记录
        
        Args:
            record_type (str): 记录类型（收入/支出）
            amount (float): 金额
            category (str): 分类
            date (datetime): 日期时间
            note (str): 备注
        
        Returns:
            bool: 是否添加成功
        """
        try:
            # 读取现有数据
            df = self.get_all_records()
            
            # 生成新ID
            new_id = df['ID'].max() + 1 if not df.empty else 1
            
            # 创建新记录
            new_record = {
                'ID': new_id,
                '类型': record_type,
                '金额': amount,
                '分类': category,
                '日期': date,
                '备注': note,
                '创建时间': datetime.now()
            }
            
            # 添加到DataFrame
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            
            # 保存到Excel
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='记账记录', index=False)
                
                # 重新格式化工作表
                worksheet = writer.sheets['记账记录']
                self._format_excel_sheet(worksheet)
            
            return True
            
        except Exception as e:
            print(f"添加记录时出错: {e}")
            return False
    
    def get_all_records(self):
        """
        获取所有记录
        
        Returns:
            pd.DataFrame: 所有记录
        """
        try:
            if os.path.exists(self.file_path):
                df = pd.read_excel(self.file_path, sheet_name='记账记录')
                # 确保日期列是datetime类型
                if '日期' in df.columns:
                    df['日期'] = pd.to_datetime(df['日期'])
                if '创建时间' in df.columns:
                    df['创建时间'] = pd.to_datetime(df['创建时间'])
                return df
            else:
                return pd.DataFrame(columns=[
                    'ID', '类型', '金额', '分类', '日期', '备注', '创建时间'
                ])
        except Exception as e:
            print(f"读取记录时出错: {e}")
            return pd.DataFrame(columns=[
                'ID', '类型', '金额', '分类', '日期', '备注', '创建时间'
            ])
    
    def delete_record(self, record_index):
        """
        删除记录
        
        Args:
            record_index (int): 记录索引
        
        Returns:
            bool: 是否删除成功
        """
        try:
            df = self.get_all_records()
            
            if record_index < 0 or record_index >= len(df):
                return False
            
            # 删除指定索引的记录
            df = df.drop(df.index[record_index]).reset_index(drop=True)
            
            # 重新分配ID
            df['ID'] = range(1, len(df) + 1)
            
            # 保存到Excel
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='记账记录', index=False)
                
                # 重新格式化工作表
                worksheet = writer.sheets['记账记录']
                self._format_excel_sheet(worksheet)
            
            return True
            
        except Exception as e:
            print(f"删除记录时出错: {e}")
            return False
    
    def clear_all_data(self):
        """
        清空所有数据
        
        Returns:
            bool: 是否清空成功
        """
        try:
            # 创建空的DataFrame
            df = pd.DataFrame(columns=[
                'ID', '类型', '金额', '分类', '日期', '备注', '创建时间'
            ])
            
            # 保存到Excel
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='记账记录', index=False)
                
                # 重新格式化工作表
                worksheet = writer.sheets['记账记录']
                self._format_excel_sheet(worksheet)
            
            return True
            
        except Exception as e:
            print(f"清空数据时出错: {e}")
            return False
    
    def get_statistics(self, start_date=None, end_date=None):
        """
        获取统计数据
        
        Args:
            start_date (datetime): 开始日期
            end_date (datetime): 结束日期
        
        Returns:
            dict: 统计数据
        """
        try:
            df = self.get_all_records()
            
            if df.empty:
                return {
                    'total_income': 0,
                    'total_expense': 0,
                    'balance': 0,
                    'record_count': 0
                }
            
            # 时间筛选
            if start_date:
                df = df[df['日期'] >= start_date]
            if end_date:
                df = df[df['日期'] <= end_date]
            
            # 计算统计
            income_df = df[df['类型'] == '收入']
            expense_df = df[df['类型'] == '支出']
            
            total_income = income_df['金额'].sum() if not income_df.empty else 0
            total_expense = expense_df['金额'].sum() if not expense_df.empty else 0
            balance = total_income - total_expense
            record_count = len(df)
            
            return {
                'total_income': total_income,
                'total_expense': total_expense,
                'balance': balance,
                'record_count': record_count
            }
            
        except Exception as e:
            print(f"获取统计数据时出错: {e}")
            return {
                'total_income': 0,
                'total_expense': 0,
                'balance': 0,
                'record_count': 0
            }
    
    def export_to_csv(self, output_path=None):
        """
        导出数据到CSV文件
        
        Args:
            output_path (str): 输出文件路径
        
        Returns:
            str: 输出文件路径
        """
        try:
            df = self.get_all_records()
            
            if output_path is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = os.path.join(self.data_dir, f"account_export_{timestamp}.csv")
            
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            return output_path
            
        except Exception as e:
            print(f"导出数据时出错: {e}")
            return None



