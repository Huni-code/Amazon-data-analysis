import pandas as pd
import numpy as np


def calculate_discount_metrics(df, metric_cols):
    return df.groupby('discount_bin', observed=False)[metric_cols].mean().reset_index()


def calculate_price_metrics(df, metric_cols):
    return df.groupby('price_bin', observed=False)[metric_cols].mean().reset_index()


def top_categories_by_metric(df, metric, n=10):
    return (
        df.groupby('main_category')[metric]
        .agg(['mean', 'median', 'count'])
        .reset_index()
        .sort_values('mean', ascending=False)
        .head(n)
    )


def discount_vs_rating_correlation(df):
    clean = df.dropna(subset=['discount_percentage', 'rating'])
    corr = clean['discount_percentage'].corr(clean['rating'])
    return {
        'correlation': round(corr, 4),
        'n_samples': len(clean),
        'discount_mean': round(clean['discount_percentage'].mean(), 2),
        'rating_mean': round(clean['rating'].mean(), 2)
    }


def price_vs_rating_correlation(df):
    clean = df.dropna(subset=['discounted_price_usd', 'rating'])
    corr = clean['discounted_price_usd'].corr(clean['rating'])
    return {
        'correlation': round(corr, 4),
        'n_samples': len(clean)
    }


def discount_vs_reviews_correlation(df):
    clean = df.dropna(subset=['discount_percentage', 'rating_count'])
    corr = clean['discount_percentage'].corr(clean['rating_count'])
    return {
        'correlation': round(corr, 4),
        'n_samples': len(clean)
    }


def category_discount_summary(df):
    summary = (
        df.groupby('main_category')
        .agg(
            product_count=('product_id', 'count'),
            avg_discount=('discount_percentage', 'mean'),
            avg_rating=('rating', 'mean'),
            avg_price=('discounted_price_usd', 'mean'),
            total_reviews=('rating_count', 'sum'),
            avg_revenue=('estimated_revenue', 'mean')
        )
        .reset_index()
        .sort_values('total_reviews', ascending=False)
    )
    return summary


def price_segment_analysis(df):
    return (
        df.groupby('price_bin', observed=False)
        .agg(
            product_count=('product_id', 'count'),
            avg_discount=('discount_percentage', 'mean'),
            avg_rating=('rating', 'mean'),
            total_reviews=('rating_count', 'sum'),
            avg_revenue=('estimated_revenue', 'mean')
        )
        .reset_index()
    )


def rating_distribution_by_discount(df):
    return (
        df.groupby(['discount_bin', 'rating_bin'], observed=False)
        .size()
        .reset_index(name='count')
    )
