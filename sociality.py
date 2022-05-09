# encoding=utf8

import pickle
import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Manager, Pool, Lock
import matplotlib
from tqdm import tqdm
from collections import Counter
from matplotlib.font_manager import *

from utils import read_texts, get_from_csv

def get_word_cnt(input_csv):
    """获取单词统计词频"""
    filepath = input_csv
    word_list = get_from_csv(filepath)
    return word_list


def compute_node_weights(co_currency):
    """获取各节点权重"""
    weights_dict = {}
    print("获取权重矩阵")
    for item in tqdm(co_currency):
        weights_dict[item[0]] = weights_dict.get(item[0], 0) + 1
        weights_dict[item[1]] = weights_dict.get(item[1], 0) + 1
    return weights_dict


def compute(contents, word_list, result_list):
    """共现统计"""
    for content in tqdm(contents):
        for i in range(len(word_list)):
            for j in range(len(word_list)):
                if i == j:
                    continue
                elif word_list[i] in content and word_list[j] in content:
                    if content.index(word_list[i]) == content.index(word_list[j]):
                        continue
                    else:
                        result_list.append((word_list[i], word_list[j]))


def get_co_currency(contents, word_list):
    """获取关键词共现情况"""

    print("计算共现矩阵")

    result = []
    compute(contents, word_list, result)
    return result[:]


def create_co_currency(text_path, word_score):
    myfont = FontProperties(fname='./word_style/STFANGSO.TTF')
    contents = read_texts(text_path)
    word_list = [item[0] for item in get_word_cnt(input_csv=word_score)]

    word_vocab = set(word_list)
    word_list = list(word_vocab)

    co_currency = get_co_currency(contents, word_list[:])  # 每条边是一个元组，构成列表
    return co_currency


def delete_item(items, co_currency):
    for key, value in tqdm(items):
        if value <= 10:
            try:
                while True:
                    co_currency.remove(key)
            except ValueError:
                continue


def filter_currency(co_currency):
    # 对共现数组进行过滤
    currency_dict = Counter(co_currency)
    items = list(currency_dict.items())
    print("\n删除低频节点：")
    delete_item(items, co_currency)
    return co_currency[:]


def simply_graph(graph0):

    # 中介中心度
    m_cent = nx.betweenness_centrality(graph0)      # 节点：中心度的映射
    cnt = 0
    # 根据中介中心度简化社会网络图
    for key, value in tqdm(sorted(m_cent.items(), key=lambda x: x[1], reverse=True)[50:]):
        graph0.remove_node(key)
        cnt += 1
    return graph0


def get_node_edge(graph0, currency_dict, word_score_dict):
    """
    获取图中的边和节点的得分，并返回结果
    :param graph0:
    :param currency_dict:
    :param word_score_dict:
    :return:
    """
    def score_processor(edge):
        """
        0, 0, 0是黑色
        255，255,255是白色
        :param.txt edge:
        :return:
        """
        if currency_dict.get(edge, 1):
            score = currency_dict.get(edge, 1)
        else:
            score = currency_dict.get(edge[::-1])

        if score >= 2:
            score *= 80
        else:
            score += 0
        score = max(min(score, 255), 30)
        return score, score, score

    edges_list = [(score_processor(edge)) for edge in graph0.edges()]
    node_score_list = [round(float(word_score_dict[node_name])*30, 4) for node_name in list(graph0.nodes())]
    return node_score_list, edges_list


def plot_image(graph0, node_score, edges_score, image_save_path):
    # kamada_kawai_layout、shell_layout、circular_layout、
    node_names = list(graph0.nodes())
    nx.draw(graph0, pos=nx.kamada_kawai_layout(graph0),
            node_color='#B0C4DE',
            labels={x: x for x in list(graph0.nodes()) if x in list(graph0.nodes())},
            nodelist=node_names,
            node_size=node_score,
            node_shape="s",
            edgelist=list(graph0.edges()),
            edge_color=list(edges_score),
            font_size=18,
            alpha=0.95)

    font = {
        'family': 'SimHei'
    }
    matplotlib.rc('font', **font)

    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False

    plt.title('词共现网络', fontsize=24)
    plt.axis('on')
    plt.savefig(image_save_path, bbox_inches='tight')
    plt.show()


def plot_social(text_path, word_score, image_save_path, simply):

    co_currency = create_co_currency(text_path, word_score)
    print(len(co_currency))

    with open("./output/currency_dict/co_currency.pkl", "wb") as fwb:
        pickle.dump(co_currency, fwb)

    # co_currency = filter_currency(co_currency)
    # with open("./output/currency_dict/co_currency_filtered.pkl", "wb") as fwb:
    #     pickle.dump(co_currency, fwb)
    #
    currency_dict = Counter(co_currency)
    word_score_dict = {item[0]: item[1] for item in get_word_cnt(input_csv=word_score)}

    graph0 = nx.Graph()
    graph0.add_edges_from(co_currency)  # 通过有权边，添加到图当中

    if simply:
        graph0 = simply_graph(graph0)

    node_score_list, edges_list = get_node_edge(graph0, currency_dict, word_score_dict)

    plot_image(graph0, node_score_list, edges_list, image_save_path)
