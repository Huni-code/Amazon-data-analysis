# 파일 경로
DATA_PATH = r'C:\Users\aa\Desktop\my Python file\amazon.csv'

# 분석 설정
EXCHANGE_RATE = 83  # 1USD = 83INR

# 할인율 구간 설정
DISCOUNT_BINS = [0, 10, 20, 30, 40, 50, 60, 100]
DISCOUNT_LABELS = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60%+']

# 가격 구간 설정
PRICE_BINS = [0, 10, 50, 100, 500, float('inf')]
PRICE_LABELS = ['~$10', '$10-50', '$50-100', '$100-500', '$500+']

# 시각화 설정
FIGURE_WIDTH = 12
FIGURE_HEIGHT = 6
OUTPUT_DIR = 'outputs'