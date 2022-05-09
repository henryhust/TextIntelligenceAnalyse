# encoding:utf-8

import os
import csv
import json
import fnmatch
from tqdm import tqdm


def read_lines(file_path):
    """read the file with lines"""
    with open(file_path, "r", encoding="utf8") as fr:
        result = []
        for line in fr.readlines():
            result.append(line.strip())
        return result


def get_stopwords():
    stopwords = []
    abs_path = os.path.abspath(os.path.dirname(__file__))
    stop_word_path = os.path.join(abs_path, "stopwords/stopwords.txt")
    with open(stop_word_path, "r", encoding="utf8") as fr:
        for line in fr.readlines():
            word = line.strip()
            stopwords.append(word)
    return stopwords


def get_from_csv(filepath):
    """读取csv文件"""
    words = []
    with open(filepath, "r", encoding="gbk") as fr:
        csv_reader = csv.reader(fr)
        for line in csv_reader:
            if not line:
                continue
            if line[0]:
                words.append((line[0], line[1]))
    return words


def read_texts(data_dir):
    """获取文本文件，并进行文本处理"""
    contents = []
    for filename in tqdm(os.listdir(data_dir)):
        if not fnmatch.fnmatch(filename, "*.txt"):
            continue

        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf8", errors='ignore') as fr:
            content = fr.read()
            contents.append(content)

    return contents


def n_lines(contents, n):
    """n行为一条文本"""
    result = []
    for i in range(0, len(contents), n):
        result.append(contents[i:i + n])
    return result

