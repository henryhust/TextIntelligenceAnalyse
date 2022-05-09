import os
dir_path = os.path.dirname(os.path.abspath(__file__))


def load_stopwords(filepath=os.path.join(dir_path, "stopwords.txt")):
    stopwords = []
    with open(filepath, encoding="utf8") as fr:
        for stopword in fr.readlines():
            stopwords.append(stopword.strip())
    return stopwords


STOPWORDS = load_stopwords()
