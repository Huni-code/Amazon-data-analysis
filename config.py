DATA_PATH = 'amazon.csv'

EXCHANGE_RATE = 83

DISCOUNT_BINS = [0, 10, 20, 30, 40, 50, 60, 100]
DISCOUNT_LABELS = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60%+']

PRICE_BINS = [0, 10, 50, 100, 500, float('inf')]
PRICE_LABELS = ['~$10', '$10-50', '$50-100', '$100-500', '$500+']

RATING_BINS = [0, 2, 3, 3.5, 4, 4.5, 5.01]
RATING_LABELS = ['0-2', '2-3', '3-3.5', '3.5-4', '4-4.5', '4.5-5']

FIGURE_WIDTH = 12
FIGURE_HEIGHT = 6
OUTPUT_DIR = 'images'
