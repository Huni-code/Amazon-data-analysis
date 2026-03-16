import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_processor import load_data, preprocess_data, get_data_summary
from analysis import (
    calculate_discount_metrics,
    category_discount_summary,
    price_segment_analysis,
    discount_vs_rating_correlation
)

st.set_page_config(
    page_title="Amazon Discount Effect Analysis",
    page_icon="📊",
    layout="wide"
)


@st.cache_data
def load_processed_data():
    raw_df = load_data()
    return preprocess_data(raw_df)


def main():
    st.title('🛒 Amazon Product Discount Effect Analysis')

    df = load_processed_data()
    summary = get_data_summary(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Products", f"{summary['total_products']:,}")
    col2.metric("Avg Discount", f"{summary['avg_discount']:.1f}%")
    col3.metric("Avg Rating", f"{summary['avg_rating']:.2f}")
    col4.metric("Avg Price", f"${summary['avg_price_usd']:.2f}")

    st.sidebar.header("Filters")
    categories = ['All'] + sorted(df['main_category'].dropna().unique().tolist())
    selected_cat = st.sidebar.selectbox("Category", categories)

    price_range = st.sidebar.slider(
        "Price Range ($)",
        0, int(df['discounted_price_usd'].max()) + 1,
        (0, int(df['discounted_price_usd'].max()) + 1)
    )

    rating_range = st.sidebar.slider("Rating", 0.0, 5.0, (0.0, 5.0), 0.1)

    filtered = df.copy()
    if selected_cat != 'All':
        filtered = filtered[filtered['main_category'] == selected_cat]
    filtered = filtered[
        (filtered['discounted_price_usd'] >= price_range[0]) &
        (filtered['discounted_price_usd'] <= price_range[1]) &
        (filtered['rating'] >= rating_range[0]) &
        (filtered['rating'] <= rating_range[1])
    ]

    st.caption(f"Showing {len(filtered):,} of {len(df):,} products")

    tab1, tab2, tab3 = st.tabs(["📊 Discount Analysis", "🏷️ Category Analysis", "💰 Price Analysis"])

    with tab1:
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Revenue by Discount Range")
            disc_rev = calculate_discount_metrics(filtered, ['estimated_revenue'])
            fig = px.bar(
                disc_rev, x='discount_bin', y='estimated_revenue',
                color='estimated_revenue', color_continuous_scale='Reds',
                labels={'discount_bin': 'Discount Range', 'estimated_revenue': 'Avg Revenue ($)'}
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("Reviews by Discount Range")
            disc_reviews = filtered.groupby('discount_bin', observed=False)['rating_count'].sum().reset_index()
            fig2 = px.pie(
                disc_reviews, names='discount_bin', values='rating_count',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Rating & Reviews by Discount")
        disc_agg = filtered.groupby('discount_bin', observed=False).agg(
            avg_rating=('rating', 'mean'),
            avg_reviews=('rating_count', 'mean')
        ).reset_index()
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(
            go.Bar(x=disc_agg['discount_bin'].astype(str), y=disc_agg['avg_reviews'],
                   name='Avg Reviews', marker_color='steelblue'),
            secondary_y=False
        )
        fig3.add_trace(
            go.Scatter(x=disc_agg['discount_bin'].astype(str), y=disc_agg['avg_rating'],
                       name='Avg Rating', mode='lines+markers', line=dict(color='red', width=3)),
            secondary_y=True
        )
        fig3.update_yaxes(title_text="Avg Review Count", secondary_y=False)
        fig3.update_yaxes(title_text="Avg Rating", secondary_y=True, range=[3.5, 4.5])
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.subheader("Category Summary")
        cat_sum = category_discount_summary(filtered)
        fig4 = px.bar(
            cat_sum.head(10), x='total_reviews', y='main_category',
            orientation='h', color='avg_revenue',
            color_continuous_scale='Viridis',
            labels={'total_reviews': 'Total Reviews', 'main_category': '', 'avg_revenue': 'Avg Revenue ($)'}
        )
        fig4.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig4, use_container_width=True)

        st.subheader("Category Bubble Chart")
        cat_top = cat_sum[cat_sum['product_count'] >= 10]
        fig5 = px.scatter(
            cat_top, x='avg_discount', y='avg_rating',
            size='total_reviews', color='avg_revenue',
            hover_name='main_category',
            color_continuous_scale='Viridis',
            labels={'avg_discount': 'Avg Discount %', 'avg_rating': 'Avg Rating'}
        )
        st.plotly_chart(fig5, use_container_width=True)

    with tab3:
        st.subheader("Price Segment Breakdown")
        price_seg = price_segment_analysis(filtered)

        col1, col2 = st.columns(2)
        with col1:
            fig6 = px.bar(
                price_seg, x='price_bin', y='avg_discount',
                color='avg_discount', color_continuous_scale='Oranges',
                labels={'price_bin': 'Price Range', 'avg_discount': 'Avg Discount %'}
            )
            fig6.update_layout(title="Avg Discount by Price")
            st.plotly_chart(fig6, use_container_width=True)

        with col2:
            fig7 = px.bar(
                price_seg, x='price_bin', y='avg_rating',
                color='avg_rating', color_continuous_scale='Greens',
                labels={'price_bin': 'Price Range', 'avg_rating': 'Avg Rating'}
            )
            fig7.update_layout(title="Avg Rating by Price", yaxis_range=[3, 5])
            st.plotly_chart(fig7, use_container_width=True)

        st.subheader("Discount vs Rating Scatter")
        fig8 = px.scatter(
            filtered.dropna(subset=['discount_percentage', 'rating']),
            x='discount_percentage', y='rating',
            color='price_bin', opacity=0.5,
            hover_data=['main_category', 'discounted_price_usd'],
            labels={'discount_percentage': 'Discount %', 'rating': 'Rating'},
            trendline='ols'
        )
        st.plotly_chart(fig8, use_container_width=True)

        corr = discount_vs_rating_correlation(filtered)
        st.info(f"Discount vs Rating Correlation: **r = {corr['correlation']}** (n = {corr['n_samples']})")


if __name__ == "__main__":
    main()
