import os
import re
import csv
import jieba
import fnmatch
from keyword_extraction import text_rank
from tqdm import tqdm
from collections import Counter
from LAC import LAC
lac = LAC(mode='lac')


def keyword_tf(input_dir, output_csv, stop_words, top_k=100):
    text = []
    for filename in tqdm(os.listdir(input_dir)):
        if not fnmatch.fnmatch(filename, "*.txt"):
            continue
        filepath = os.path.join(input_dir, filename)
        with open(filepath, "r", encoding="utf8", errors='ignore') as fr:
            content = fr.read().replace(" ", "")
            content = " ".join(re.findall(u'[\u4e00-\u9fa5]+', content))            # 去除无效字符
            content_list = [word for word in lac.run(content) if word not in stop_words and len(word) > 1]
            text.extend(content_list)
    word_counts = Counter(text)
    word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    with open(output_csv, "w", newline="") as fw:
        csv_writer = csv.writer(fw)
        for item in word_counts[:top_k]:
            csv_writer.writerow(item)
    return word_counts


def keyword_extraction(input_dir, output_csv, stop_words, top_k=20):
    """textRank关键词抽取"""
    all_keywords = []
    text = []
    for filename in tqdm(os.listdir(input_dir)):
        if not fnmatch.fnmatch(filename, "*.txt"):
            continue
        filepath = os.path.join(input_dir, filename)
        with open(filepath, "r", encoding="utf8", errors='ignore') as fr:
            content = fr.read()

            content_list = [word for word in lac.run(content)[0] if word not in stop_words and len(word) > 1]
            text.extend(content_list)

            keywords = text_rank.textrank(content, withWeight=True, topK=top_k)
            keywords = [word[0] for word in keywords if word[0].strip() not in stop_words]
            all_keywords.extend(keywords)

    all_keywords = list(set(all_keywords))
    word_counts = Counter(text)

    result = [(item, word_counts.get(item)) for item in all_keywords]
    result = sorted(result, key=lambda x: x[1], reverse=True)

    with open(output_csv, "w", newline="") as fw:
        csv_writer = csv.writer(fw)

        for item in result:
            csv_writer.writerow(item)