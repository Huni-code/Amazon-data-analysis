# Amazon Product Discount Effect Analysis

**Sunghun Kim**

Analyzing how discount rates affect revenue, ratings, review volume, and purchase behavior across 1,465 Amazon India products.

---

## About

This project explores the relationship between discount percentages and key business metrics using Amazon product listing data. All prices are converted from INR to USD. The analysis covers discount impact on revenue, category-level comparisons, price segment behavior, and correlation analysis.

The project includes static visualizations (matplotlib/seaborn) and an interactive Streamlit dashboard with filtering by category, price range, and rating.

---

## Dataset

- **Source**: Amazon India product listings (Kaggle)
- **Size**: 1,465 products across 9 categories
- **Features**: product name, category, discounted/actual price, discount %, rating, review count

| Stat | Value |
|------|:---:|
| Avg Discount | 47.7% |
| Avg Rating | 4.10 |
| Avg Price | $37.65 |
| Median Price | $9.63 |
| Total Reviews | 26.8M |

---

## Key Findings

### 1. Revenue by Discount Range

![Fig 1](images/fig1_revenue_by_discount.png)

Products in the **0–10% discount range** generate the highest estimated revenue. Lightly discounted or premium products drive more revenue per unit than heavily discounted ones.

### 2. Review Volume by Discount

![Fig 2](images/fig2_reviews_by_discount_pie.png)

The **60%+** and **40–50%** ranges attract the most reviews, suggesting deep discounts drive higher purchase volume (using review count as a sales proxy).

### 3. Price & Discount Distributions

![Fig 3](images/fig3_distributions.png)

Prices are heavily right-skewed (median $9.63 vs mean $37.65). Most products fall in the 40–60% discount range.

### 4. Top Categories by Review Volume

![Fig 4](images/fig4_top_categories.png)

Electronics dominates with 15.8M reviews, followed by Computers & Accessories (7.7M) and Home & Kitchen (3.0M).

### 5. Price Segment Analysis

![Fig 5](images/fig5_price_segments.png)

Cheaper products get deeper discounts (53.5% for ~$10 vs 31% for $500+). Higher-priced products have slightly better ratings and significantly higher revenue per product.

### 6. Correlation Analysis

![Fig 6](images/fig6_correlations.png)

| Relationship | Correlation (r) | Interpretation |
|-------------|:---:|----------------|
| Discount vs Rating | -0.155 | Weak negative — higher discounts slightly associate with lower ratings |
| Price vs Rating | +0.120 | Weak positive — pricier products rate slightly higher |
| Discount vs Reviews | +0.012 | Near zero — discount alone doesn't drive review count |

### 7. Discount × Rating Heatmap

![Fig 7](images/fig7_heatmap.png)

Most products cluster in the 40–60% discount range with 4.0–4.5 ratings. Very few products exist in extreme discount or low rating ranges.

### 8. Category Bubble Chart

![Fig 8](images/fig8_category_bubble.png)

Categories compared by average discount, rating, review volume (bubble size), and revenue (color). Electronics has the highest revenue despite moderate ratings.

### 9. Rating & Reviews by Discount

![Fig 9](images/fig9_rating_reviews_by_discount.png)

Dual-axis view showing that review counts peak at 50–60% discounts, while average ratings remain relatively stable across all discount ranges.

---

## Insights Summary

- Premium-priced, lightly discounted products generate the most revenue per unit
- Deep discounts (60%+) drive purchase volume but not revenue
- Discount percentage has weak correlation with ratings — discounting doesn't hurt product perception
- Higher-priced products tend to have slightly better ratings and much higher revenue
- Electronics is the dominant category by every metric

---

## Project Structure

```
Amazon-data-analysis/
├── main.py              # Static analysis (9 figures)
├── dashboard.py         # Streamlit interactive dashboard
├── data_processor.py    # Data loading, cleaning, feature engineering
├── analysis.py          # Analysis functions
├── config.py            # Settings (bins, exchange rate, paths)
├── amazon.csv           # Dataset
└── images/              # Generated visualizations
```

---

## How to Run

### Static Analysis
```bash
pip install pandas matplotlib seaborn numpy tabulate
python main.py
```

### Interactive Dashboard
```bash
pip install streamlit plotly statsmodels
streamlit run dashboard.py
```

---

## Tech Stack

- Python 3, Pandas, NumPy
- Matplotlib, Seaborn (static charts)
- Streamlit, Plotly (interactive dashboard)
