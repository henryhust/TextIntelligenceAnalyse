from frequence import keyword_tf, keyword_extraction
from utils import get_stopwords
from sociality import plot_social


STOP_WORDS = get_stopwords()


if __name__ == '__main__':
    # 词频统计
    # keyword_tf(input_dir="./data", output_csv="./output/keywords.csv", stop_words=STOP_WORDS)
    keyword_extraction(input_dir="./data", output_csv="./output/keywords.csv", stop_words=STOP_WORDS)
    # 词共现计算，并绘制共现网络图
    plot_social(text_path="./data", word_score="./output/keywords.csv", image_save_path="output/词共现网络图.png", simply=False)
