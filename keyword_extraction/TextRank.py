import jieba
from jieba.posseg import pair
from jieba.analyse.tfidf import KeywordExtractor
from jieba.analyse.textrank import UndirectWeightedGraph
from collections import defaultdict
from operator import itemgetter
from LAC import LAC

lac = LAC(mode="lac")


class TextRank(KeywordExtractor):

    def __init__(self):
        # self.tokenizer = self.postokenizer = jieba.posseg.dt
        self.tokenizer = self.postokenizer = lac
        self.stop_words = self.STOP_WORDS.copy()
        self.pos_filt = frozenset(('ns', 'n', 'vn', 'v'))
        self.span = 5

    def pairfilter(self, wp):
        return (wp.flag in self.pos_filt and len(wp.word.strip()) >= 2
                and wp.word.lower() not in self.stop_words)

    def textrank(self, sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v', 'LOC'), withFlag=False):
        """
        Extract keywords from sentence using TextRank algorithm.
        Parameter:
            - topK: return how many top keywords. `None` for all possible words.
            - withWeight: if True, return a list of (word, weight);
                          if False, return a list of words.
            - allowPOS: the allowed POS list eg. ['ns', 'n', 'vn', 'v'].
                        if the POS of w is not in this list, it will be filtered.
            - withFlag: if True, return a list of pair(word, weight) like posseg.cut
                        if False, return a list of words
        """
        self.pos_filt = frozenset(allowPOS)
        g = UndirectWeightedGraph()
        cm = defaultdict(int)           # 统计共现词频
        # words = tuple(self.tokenizer.cut(sentence))
        words = [pair(item[0], item[1]) for item in zip(*self.tokenizer.run(sentence))]
        for i, wp in enumerate(words):
            if self.pairfilter(wp):
                for j in range(i + 1, i + self.span):
                    if j >= len(words):
                        break
                    if not self.pairfilter(words[j]):
                        continue
                    if allowPOS and withFlag:
                        cm[(wp, words[j])] += 1
                    else:
                        cm[(wp.word, words[j].word)] += 1

        for terms, w in cm.items():
            g.addEdge(terms[0], terms[1], w)
        nodes_rank = g.rank()
        if withWeight:
            tags = sorted(nodes_rank.items(), key=itemgetter(1), reverse=True)
        else:
            tags = sorted(nodes_rank, key=nodes_rank.__getitem__, reverse=True)

        if topK:
            return tags[:topK]
        else:
            return tags

    extract_tags = textrank
