# main.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from data_processor import load_data, preprocess_data
from analysis import calculate_discount_metrics
from config import OUTPUT_DIR

def visualize_overall_revenue_by_discount(df):
    # 할인율에 따른 매출 분석
    discount_sales = calculate_discount_metrics(df, ['estimated_revenue'])
    
    # 직접 그래프 그리기
    plt.figure(figsize=(12, 6))
    plt.bar(discount_sales['discount_bin'], discount_sales['estimated_revenue'], color='salmon')
    plt.title('Average Revenue by Discount Range (USD)')
    plt.xlabel('Discount Range')
    plt.ylabel('Average Revenue ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def visualize_discount_review_pie(df):
    # 할인율 구간별 리뷰 수 계산
    discount_reviews = df.groupby('discount_bin')['rating_count'].sum().reset_index()
    
    # 파이차트 생성
    plt.figure(figsize=(10, 10))
    plt.pie(discount_reviews['rating_count'], 
            labels=discount_reviews['discount_bin'],
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Paired(np.linspace(0, 1, len(discount_reviews))))
    
    plt.axis('equal')  # 원형으로 보이게 설정
    plt.title('Distribution of Reviews by Discount Range', fontsize=16)
    
    plt.show()

def main():
    """메인 함수"""
    # 데이터 로드 및 전처리
    raw_df = load_data()
    df = preprocess_data(raw_df)
    
    # 할인율-매출 
    visualize_overall_revenue_by_discount(df)
    
    # 할인율-리뷰 수
    visualize_discount_review_pie(df)

if __name__ == "__main__":
    main()

print("daebak")