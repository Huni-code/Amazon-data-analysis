# visualizers.py
import matplotlib.pyplot as plt
import seaborn as sns
from config import FIGURE_WIDTH, FIGURE_HEIGHT

def plot_discount_vs_metric(df, metric, title, xlabel='Discount Range', ylabel=None, color='blue'):
    """할인율에 따른 지표 막대 그래프"""
    if ylabel is None:
        ylabel = f'Average {metric}'
    
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    sns.barplot(x='discount_bin', y=metric, data=df, color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.show()