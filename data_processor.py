import pandas as pd
import numpy as np
from config import (
    DATA_PATH, EXCHANGE_RATE,
    DISCOUNT_BINS, DISCOUNT_LABELS,
    PRICE_BINS, PRICE_LABELS,
    RATING_BINS, RATING_LABELS
)


def load_data():
    df = pd.read_csv(DATA_PATH, encoding='utf-8')
    return df


def convert_rupees_to_usd(price_str):
    try:
        price = float(str(price_str).replace('₹', '').replace(',', ''))
        return round(price / EXCHANGE_RATE, 2)
    except (ValueError, AttributeError):
        return np.nan


def extract_main_category(cat_str):
    try:
        return str(cat_str).split('|')[0]
    except (AttributeError, IndexError):
        return 'Unknown'


def extract_sub_category(cat_str):
    try:
        parts = str(cat_str).split('|')
        return parts[1] if len(parts) > 1 else parts[0]
    except (AttributeError, IndexError):
        return 'Unknown'


def preprocess_data(df):
    df = df.copy()

    df['discounted_price_usd'] = df['discounted_price'].apply(convert_rupees_to_usd)
    df['actual_price_usd'] = df['actual_price'].apply(convert_rupees_to_usd)

    df['discount_percentage'] = (
        df['discount_percentage'].astype(str).str.replace('%', '')
    )
    df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')

    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['rating_count'] = (
        df['rating_count'].astype(str).str.replace(',', '')
    )
    df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

    df['discount_bin'] = pd.cut(
        df['discount_percentage'],
        bins=DISCOUNT_BINS,
        labels=DISCOUNT_LABELS
    )

    df['price_bin'] = pd.cut(
        df['discounted_price_usd'],
        bins=PRICE_BINS,
        labels=PRICE_LABELS
    )

    df['rating_bin'] = pd.cut(
        df['rating'],
        bins=RATING_BINS,
        labels=RATING_LABELS
    )

    df['main_category'] = df['category'].apply(extract_main_category)
    df['sub_category'] = df['category'].apply(extract_sub_category)

    df['estimated_revenue'] = df['rating_count'] * df['discounted_price_usd']

    df['discount_amount_usd'] = df['actual_price_usd'] - df['discounted_price_usd']

    df['savings_ratio'] = np.where(
        df['actual_price_usd'] > 0,
        df['discount_amount_usd'] / df['actual_price_usd'],
        0
    )

    return df


def get_data_summary(df):
    summary = {
        'total_products': len(df),
        'categories': df['main_category'].nunique(),
        'avg_discount': df['discount_percentage'].mean(),
        'avg_rating': df['rating'].mean(),
        'avg_price_usd': df['discounted_price_usd'].mean(),
        'median_price_usd': df['discounted_price_usd'].median(),
        'total_reviews': df['rating_count'].sum(),
        'missing_values': df[['discount_percentage', 'rating', 'rating_count', 'discounted_price_usd']].isnull().sum().to_dict()
    }
    return summary
