# data_processor.py
import pandas as pd
from config import DATA_PATH, EXCHANGE_RATE, DISCOUNT_BINS, DISCOUNT_LABELS

def load_data():
    df = pd.read_csv(DATA_PATH, encoding='utf-8')
    return df

def preprocess_data(df):
    
    # 데이터 복사본 생성
    df = df.copy()
    
    # 가격 데이터 변환 (루피 -> 달러)
    df['discounted_price_usd'] = df['discounted_price'].apply(convert_rupees_to_usd)
    
    # 할인 비율 숫자로 변환
    df['discount_percentage'] = df['discount_percentage'].str.replace('%', '').astype(float)
    
    # 리뷰 수(판매량 지표) 숫자로 변환
    df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')
    
    # 할인율 구간 생성
    df['discount_bin'] = pd.cut(
        df['discount_percentage'], 
        bins=DISCOUNT_BINS,
        labels=DISCOUNT_LABELS
    )
    
    # 판매량 추정
    df['estimated_sales'] = df['rating_count']
    
    # 추정 매출 계산
    df['estimated_revenue'] = df['estimated_sales'] * df['discounted_price_usd']
    
    return df

def convert_rupees_to_usd(price_str):
    """루피 가격을 USD로 변환."""
    price = float(price_str.replace('₹', '').replace(',', ''))
    return round(price / EXCHANGE_RATE, 2)