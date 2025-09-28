import streamlit as st
import pandas as pd
import datetime
from src.data_manager import DataManager
import plotly.express as px
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="我的记账本",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
    }
    .expense-card {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f44336;
    }
    .income-card {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
    }
    .stButton > button {
        background-color: #2E86AB;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #1e5f7a;
    }
</style>
""", unsafe_allow_html=True)

# 初始化数据管理器
@st.cache_resource
def get_data_manager():
    return DataManager()

data_manager = get_data_manager()

def main():
    # 主标题
    st.markdown('<h1 class="main-header">💰 我的记账本</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.markdown("## 📊 功能菜单")
        page = st.selectbox(
            "选择功能",
            ["📝 记账", "📈 统计", "📋 记录查看", "⚙️ 设置"]
        )
        
        st.markdown("---")
        st.markdown("## 💡 使用提示")
        st.info("点击上方菜单选择不同功能")
    
    # 根据选择显示不同页面
    if page == "📝 记账":
        show_add_record_page()
    elif page == "📈 统计":
        show_statistics_page()
    elif page == "📋 记录查看":
        show_records_page()
    elif page == "⚙️ 设置":
        show_settings_page()

def show_add_record_page():
    st.markdown("## 📝 添加记账记录")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 记录类型
        record_type = st.radio(
            "记录类型",
            ["💸 支出", "💰 收入"],
            horizontal=True
        )
        
        # 金额输入
        amount = st.number_input(
            "金额 (元)",
            min_value=0.01,
            step=0.01,
            format="%.2f"
        )
        
        # 分类选择
        if record_type == "💸 支出":
            category = st.selectbox(
                "支出分类",
                ["🍽️ 餐饮", "🚗 交通", "🛒 购物", "🏠 住房", "💊 医疗", "🎮 娱乐", "📚 教育", "其他"]
            )
        else:
            category = st.selectbox(
                "收入分类",
                ["💼 工资", "💹 投资", "🎁 奖金", "💸 其他收入"]
            )
    
    with col2:
        # 日期选择
        date = st.date_input(
            "日期",
            value=datetime.date.today()
        )
        
        # 时间选择
        time = st.time_input(
            "时间",
            value=datetime.datetime.now().time()
        )
        
        # 备注
        note = st.text_area(
            "备注",
            placeholder="添加备注信息...",
            height=100
        )
    
    # 提交按钮
    if st.button("💾 保存记录", type="primary"):
        if amount > 0:
            # 组合日期和时间
            datetime_obj = datetime.datetime.combine(date, time)
            
            # 保存记录
            success = data_manager.add_record(
                record_type="支出" if record_type == "💸 支出" else "收入",
                amount=amount,
                category=category,
                date=datetime_obj,
                note=note
            )
            
            if success:
                st.success("✅ 记录保存成功！")
                st.rerun()
            else:
                st.error("❌ 保存失败，请重试")
        else:
            st.warning("⚠️ 请输入有效的金额")

def show_statistics_page():
    st.markdown("## 📈 统计分析")
    
    # 获取数据
    df = data_manager.get_all_records()
    
    if df.empty:
        st.info("📊 暂无数据，请先添加一些记录")
        return
    
    # 时间范围选择
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "开始日期",
            value=df['日期'].min().date() if not df.empty else datetime.date.today()
        )
    with col2:
        end_date = st.date_input(
            "结束日期",
            value=df['日期'].max().date() if not df.empty else datetime.date.today()
        )
    
    # 筛选数据
    df_filtered = df[
        (df['日期'].dt.date >= start_date) & 
        (df['日期'].dt.date <= end_date)
    ]
    
    if df_filtered.empty:
        st.warning("⚠️ 所选时间范围内没有数据")
        return
    
    # 计算统计信息
    total_income = df_filtered[df_filtered['类型'] == '收入']['金额'].sum()
    total_expense = df_filtered[df_filtered['类型'] == '支出']['金额'].sum()
    balance = total_income - total_expense
    
    # 显示统计卡片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="income-card">', unsafe_allow_html=True)
        st.metric("💰 总收入", f"¥{total_income:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="expense-card">', unsafe_allow_html=True)
        st.metric("💸 总支出", f"¥{total_expense:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("💳 结余", f"¥{balance:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 图表展示
    col1, col2 = st.columns(2)
    
    with col1:
        # 收支趋势图
        daily_data = df_filtered.groupby([df_filtered['日期'].dt.date, '类型'])['金额'].sum().unstack(fill_value=0)
        
        if not daily_data.empty:
            fig = go.Figure()
            if '收入' in daily_data.columns:
                fig.add_trace(go.Scatter(
                    x=daily_data.index,
                    y=daily_data['收入'],
                    mode='lines+markers',
                    name='收入',
                    line=dict(color='#4caf50', width=3)
                ))
            if '支出' in daily_data.columns:
                fig.add_trace(go.Scatter(
                    x=daily_data.index,
                    y=daily_data['支出'],
                    mode='lines+markers',
                    name='支出',
                    line=dict(color='#f44336', width=3)
                ))
            
            fig.update_layout(
                title="📈 收支趋势",
                xaxis_title="日期",
                yaxis_title="金额 (元)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 支出分类饼图
        expense_data = df_filtered[df_filtered['类型'] == '支出']
        if not expense_data.empty:
            category_data = expense_data.groupby('分类')['金额'].sum()
            
            fig = px.pie(
                values=category_data.values,
                names=category_data.index,
                title="💸 支出分类分布",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

def show_records_page():
    st.markdown("## 📋 记录查看")
    
    # 获取数据
    df = data_manager.get_all_records()
    
    if df.empty:
        st.info("📊 暂无记录，请先添加一些记录")
        return
    
    # 筛选选项
    col1, col2, col3 = st.columns(3)
    
    with col1:
        record_type_filter = st.selectbox(
            "记录类型",
            ["全部", "收入", "支出"]
        )
    
    with col2:
        category_filter = st.selectbox(
            "分类",
            ["全部"] + list(df['分类'].unique())
        )
    
    with col3:
        sort_by = st.selectbox(
            "排序方式",
            ["日期降序", "日期升序", "金额降序", "金额升序"]
        )
    
    # 筛选数据
    filtered_df = df.copy()
    
    if record_type_filter != "全部":
        filtered_df = filtered_df[filtered_df['类型'] == record_type_filter]
    
    if category_filter != "全部":
        filtered_df = filtered_df[filtered_df['分类'] == category_filter]
    
    # 排序
    if sort_by == "日期降序":
        filtered_df = filtered_df.sort_values('日期', ascending=False)
    elif sort_by == "日期升序":
        filtered_df = filtered_df.sort_values('日期', ascending=True)
    elif sort_by == "金额降序":
        filtered_df = filtered_df.sort_values('金额', ascending=False)
    elif sort_by == "金额升序":
        filtered_df = filtered_df.sort_values('金额', ascending=True)
    
    # 格式化显示
    display_df = filtered_df.copy()
    display_df['日期'] = display_df['日期'].dt.strftime('%Y-%m-%d %H:%M')
    display_df['金额'] = display_df['金额'].apply(lambda x: f"¥{x:.2f}")
    
    # 显示记录
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # 删除记录功能
    st.markdown("---")
    st.markdown("### 🗑️ 删除记录")
    
    if not filtered_df.empty:
        record_to_delete = st.selectbox(
            "选择要删除的记录",
            range(len(filtered_df)),
            format_func=lambda x: f"{filtered_df.iloc[x]['日期'].strftime('%Y-%m-%d %H:%M')} - {filtered_df.iloc[x]['类型']} - {filtered_df.iloc[x]['分类']} - ¥{filtered_df.iloc[x]['金额']:.2f}"
        )
        
        if st.button("🗑️ 删除选中记录", type="secondary"):
            if data_manager.delete_record(record_to_delete):
                st.success("✅ 记录删除成功！")
                st.rerun()
            else:
                st.error("❌ 删除失败，请重试")

def show_settings_page():
    st.markdown("## ⚙️ 设置")
    
    st.markdown("### 📊 数据管理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 导出数据", type="primary"):
            df = data_manager.get_all_records()
            if not df.empty:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="💾 下载CSV文件",
                    data=csv,
                    file_name=f"记账数据_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("⚠️ 暂无数据可导出")
    
    with col2:
        if st.button("🗑️ 清空所有数据", type="secondary"):
            if st.checkbox("确认清空所有数据（此操作不可恢复）"):
                if data_manager.clear_all_data():
                    st.success("✅ 数据已清空")
                    st.rerun()
                else:
                    st.error("❌ 清空失败")
    
    st.markdown("---")
    st.markdown("### ℹ️ 关于")
    st.info("""
    **我的记账本 v1.0**
    
    - 使用 Streamlit 开发
    - 数据存储在 Excel 文件中
    - 支持收支记录、统计分析、数据导出等功能
    
    💡 **使用提示：**
    - 定期备份数据文件
    - 建议每月导出一次数据
    - 数据文件位置：`data/account_records.xlsx`
    """)

if __name__ == "__main__":
    main()



