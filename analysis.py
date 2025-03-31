# analysis.py
import pandas as pd

def calculate_discount_metrics(df, metric_cols):
    """할인율 구간별 지표 계산"""
    return df.groupby('discount_bin', observed=False)[metric_cols].mean().reset_index()