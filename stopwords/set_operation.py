#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-05-09 11:15
# @Author  : henry
# @Site    : http:github.com/henryhust
# @File    : set_operation.py

with open("../old/keywords.txt", "r", encoding="utf8") as fr1, open("../old/keywords_1.txt", "r", encoding="utf8") as fr2:
    keywords = []
    all_words = []
    for line in fr1.readlines():
        keywords.append(line.strip().split("\t")[0])
    for line in fr2.readlines():
        all_words.append(line.strip().split("\t")[0])
    result = set(keywords)-set(all_words)
    for word in result:
        print(word)