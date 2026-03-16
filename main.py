import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_processor import load_data, preprocess_data, get_data_summary
from analysis import (
    calculate_discount_metrics,
    calculate_price_metrics,
    top_categories_by_metric,
    discount_vs_rating_correlation,
    price_vs_rating_correlation,
    discount_vs_reviews_correlation,
    category_discount_summary,
    price_segment_analysis,
    rating_distribution_by_discount
)
from config import OUTPUT_DIR
import os

os.makedirs(OUTPUT_DIR, exist_ok=True)
sns.set_style("whitegrid")


def main():
    raw_df = load_data()
    df = preprocess_data(raw_df)

    print("=" * 60)
    print("AMAZON PRODUCT DISCOUNT EFFECT ANALYSIS")
    print("=" * 60)

    summary = get_data_summary(df)
    print(f"\nTotal Products: {summary['total_products']}")
    print(f"Categories: {summary['categories']}")
    print(f"Average Discount: {summary['avg_discount']:.1f}%")
    print(f"Average Rating: {summary['avg_rating']:.2f}")
    print(f"Average Price: ${summary['avg_price_usd']:.2f}")
    print(f"Median Price: ${summary['median_price_usd']:.2f}")
    print(f"Total Reviews: {summary['total_reviews']:,.0f}")
    print(f"\nMissing Values: {summary['missing_values']}")

    # ── Fig 1: Revenue by Discount Range ──
    print("\n[1/9] Revenue by Discount Range")
    discount_rev = calculate_discount_metrics(df, ['estimated_revenue'])
    plt.figure(figsize=(10, 6))
    plt.bar(discount_rev['discount_bin'].astype(str), discount_rev['estimated_revenue'], color='salmon')
    plt.title('Fig 1: Average Estimated Revenue by Discount Range')
    plt.xlabel('Discount Range')
    plt.ylabel('Average Revenue ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig1_revenue_by_discount.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Fig 2: Review Distribution by Discount (Pie) ──
    print("[2/9] Review Distribution by Discount")
    discount_reviews = df.groupby('discount_bin', observed=False)['rating_count'].sum().reset_index()
    plt.figure(figsize=(8, 8))
    colors = plt.cm.Paired(np.linspace(0, 1, len(discount_reviews)))
    plt.pie(
        discount_reviews['rating_count'],
        labels=discount_reviews['discount_bin'],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors
    )
    plt.title('Fig 2: Distribution of Reviews by Discount Range')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig2_reviews_by_discount_pie.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Fig 3: Price Distribution ──
    print("[3/9] Price Distribution")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    df['discounted_price_usd'].dropna().clip(upper=200).plot(
        kind='hist', bins=50, ax=axes[0], edgecolor='black', color='steelblue'
    )
    axes[0].set_title('Fig 3a: Discounted Price Distribution (USD)')
    axes[0].set_xlabel('Price ($)')
    axes[0].axvline(df['discounted_price_usd'].median(), color='red', linestyle='--', label=f"Median: ${df['discounted_price_usd'].median():.0f}")
    axes[0].legend()

    df['discount_percentage'].dropna().plot(
        kind='hist', bins=30, ax=axes[1], edgecolor='black', color='coral'
    )
    axes[1].set_title('Fig 3b: Discount Percentage Distribution')
    axes[1].set_xlabel('Discount %')
    axes[1].axvline(df['discount_percentage'].median(), color='red', linestyle='--', label=f"Median: {df['discount_percentage'].median():.0f}%")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig3_distributions.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Fig 4: Top 10 Categories by Revenue ──
    print("[4/9] Top Categories by Revenue")
    cat_summary = category_discount_summary(df)
    top10 = cat_summary.head(10)
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top10['main_category'][::-1], top10['total_reviews'][::-1], color='teal')
    plt.title('Fig 4: Top 10 Categories by Total Reviews')
    plt.xlabel('Total Reviews')
    for bar, rev in zip(bars, top10['avg_revenue'][::-1]):
        plt.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
                 f'Avg Rev: ${rev:,.0f}', va='center', fontsize=9, color='gray')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig4_top_categories.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Fig 5: Price Segment Analysis ──
    print("[5/9] Price Segment Analysis")
    price_seg = price_segment_analysis(df)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    axes[0].bar(price_seg['price_bin'].astype(str), price_seg['avg_discount'], color='orange')
    axes[0].set_title('Avg Discount by Price Segment')
    axes[0].set_ylabel('Discount %')
    axes[0].set_xlabel('Price Range')

    axes[1].bar(price_seg['price_bin'].astype(str), price_seg['avg_rating'], color='green')
    axes[1].set_title('Avg Rating by Price Segment')
    axes[1].set_ylabel('Rating')
    axes[1].set_ylim(3, 5)
    axes[1].set_xlabel('Price Range')

    axes[2].bar(price_seg['price_bin'].astype(str), price_seg['product_count'], color='steelblue')
    axes[2].set_title('Product Count by Price Segment')
    axes[2].set_ylabel('Count')
    axes[2].set_xlabel('Price Range')

    plt.suptitle('Fig 5: Price Segment Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig5_price_segments.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Fig 6: Discount vs Rating Scatter ──
    print("[6/9] Discount vs Rating Correlation")
    corr_dr = discount_vs_rating_correlation(df)
    corr_pr = price_vs_rating_correlation(df)
    corr_drev = discount_vs_reviews_correlation(df)

    print(f"  Discount vs Rating: r = {corr_dr['correlation']}")
    print(f"  Price vs Rating:    r = {corr_pr['correlation']}")
    print(f"  Discount vs Reviews: r = {corr_drev['correlation']}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    clean = df.dropna(subset=['discount_percentage', 'rating'])
    axes[0].scatter(clean['discount_percentage'], clean['rating'], alpha=0.3, s=15, color='coral')
    z = np.polyfit(clean['discount_percentage'], clean['rating'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(clean['discount_percentage'].min(), clean['discount_percentage'].max(), 100)
    axes[0].plot(x_line, p(x_line), color='red', linewidth=2)
    axes[0].set_title(f'Fig 6a: Discount % vs Rating (r = {corr_dr["correlation"]})')
    axes[0].set_xlabel('Discount %')
    axes[0].set_ylabel('Rating')

    clean2 = df.dropna(subset=['discounted_price_usd', 'rating'])
    clean2 = clean2[clean2['discounted_price_usd'] < 300]
    axes[1].scatter(clean2['discounted_price_usd'], clean2['rating'], alpha=0.3, s=15, color='steelblue')
    z2 = np.polyfit(clean2['discounted_price_usd'], clean2['rating'], 1)
    p2 = np.poly1d(z2)
    x_line2 = np.linspace(clean2['discounted_price_usd'].min(), clean2['discounted_price_usd'].max(), 100)
    axes[1].plot(x_line2, p2(x_line2), color='red', linewidth=2)
    axes[1].set_title(f'Fig 6b: Price vs Rating (r = {corr_pr["correlation"]})')
    axes[1].set_xlabel('Price ($)')
    axes[1].set_ylabel('Rating')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig6_correlations.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Fig 7: Heatmap - Discount vs Rating ──
    print("[7/9] Rating Distribution Heatmap")
    rating_dist = rating_distribution_by_discount(df)
    pivot = rating_dist.pivot_table(index='rating_bin', columns='discount_bin', values='count', fill_value=0)
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd')
    plt.title('Fig 7: Product Count by Discount Range and Rating')
    plt.xlabel('Discount Range')
    plt.ylabel('Rating Range')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig7_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Fig 8: Category Comparison ──
    print("[8/9] Category Discount vs Rating")
    cat_top = cat_summary[cat_summary['product_count'] >= 20].head(8)
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        cat_top['avg_discount'],
        cat_top['avg_rating'],
        s=cat_top['total_reviews'] / 500,
        c=cat_top['avg_revenue'],
        cmap='viridis',
        alpha=0.7,
        edgecolors='black'
    )
    for _, row in cat_top.iterrows():
        label = row['main_category'][:20]
        ax.annotate(label, (row['avg_discount'], row['avg_rating']),
                    fontsize=8, ha='center', va='bottom')
    plt.colorbar(scatter, label='Avg Revenue ($)')
    ax.set_title('Fig 8: Category Comparison (size = review volume)')
    ax.set_xlabel('Average Discount %')
    ax.set_ylabel('Average Rating')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig8_category_bubble.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Fig 9: Avg Rating & Review Count by Discount ──
    print("[9/9] Rating and Reviews by Discount")
    disc_metrics = df.groupby('discount_bin', observed=False).agg(
        avg_rating=('rating', 'mean'),
        avg_reviews=('rating_count', 'mean')
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 6))
    x = range(len(disc_metrics))
    bars = ax1.bar(x, disc_metrics['avg_reviews'], color='steelblue', alpha=0.7, label='Avg Review Count')
    ax1.set_xlabel('Discount Range')
    ax1.set_ylabel('Avg Review Count', color='steelblue')
    ax1.set_xticks(x)
    ax1.set_xticklabels(disc_metrics['discount_bin'].astype(str), rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(x, disc_metrics['avg_rating'], color='red', marker='o', linewidth=2, label='Avg Rating')
    ax2.set_ylabel('Avg Rating', color='red')
    ax2.set_ylim(3.5, 4.5)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    plt.title('Fig 9: Average Review Count and Rating by Discount Range')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig9_rating_reviews_by_discount.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Summary Table ──
    print("\n" + "=" * 60)
    print("CATEGORY SUMMARY")
    print("=" * 60)
    print(cat_summary[['main_category', 'product_count', 'avg_discount', 'avg_rating', 'avg_price', 'total_reviews']].to_markdown(index=False, numalign='left', stralign='left', floatfmt='.2f'))

    print("\n" + "=" * 60)
    print("PRICE SEGMENT SUMMARY")
    print("=" * 60)
    print(price_seg.to_markdown(index=False, numalign='left', stralign='left', floatfmt='.2f'))

    print(f"\nAll figures saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
