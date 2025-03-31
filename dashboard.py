# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from data_processor import load_data, preprocess_data
from analysis import calculate_discount_metrics

# 페이지 설정
st.set_page_config(
    page_title="Amazon Discount Effect Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# 데이터 로드 및 전처리
@st.cache_data
def load_processed_data():
    raw_df = load_data()
    return preprocess_data(raw_df)

# 메인 함수
def main():
    st.title('🛒 Amazon Product Discount Effect Analysis Dashboard')
    
    # 데이터 로드
    df = load_processed_data()
    
    # 할인율에 따른 매출 차트
    st.header('Average Revenue by Discount Range')
    discount_sales = calculate_discount_metrics(df, ['estimated_revenue'])
    
    fig = px.bar(
        discount_sales, 
        x='discount_bin', 
        y='estimated_revenue',
        color='estimated_revenue',
        labels={'discount_bin': 'Discount Range', 'estimated_revenue': 'Average Revenue ($)'},
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()