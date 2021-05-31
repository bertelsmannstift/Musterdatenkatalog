import os
from io import StringIO

import spacy
import pandas as pd
from charsplit import Splitter
from html.parser import HTMLParser

REMOVE_WORDS_PATH = os.path.join(os.path.dirname(__file__), "remove_words.csv")
REMOVE_WORDS = pd.read_csv(REMOVE_WORDS_PATH, header=None)[0].apply(lambda x: x.lower()).values
nlp = spacy.load("de_core_news_lg")


def remove_word_and_underscore_transformer(ser):
    ser = ser.apply(remove_words)
    return ser.apply(lambda x: x.replace("_", " "))


def split_words(text):
    output = []
    splitter = Splitter()
    for word in text.split():
        output.append(word)
        results = splitter.split_compound(word)
        for result in results:
            if result[0] > 0.5:
                output.append(result[1])
                output.append(result[2])
    return " ".join(output)


def compound_word_transformer(ser):
    return ser.apply(split_words)


def lemmatize_pipe(doc):
    lemma_list = [str(tok.lemma_).lower() for tok in nlp(doc)
                  if tok.is_alpha and not (tok.is_stop or tok.is_punct or tok.is_space)]
    return " ".join(lemma_list)


def spacy_lemmatize_transformer(ser):
    return ser.apply(lemmatize_pipe)


def remove_words(doc):
    x = [tok for tok in doc.split() if tok.lower() not in REMOVE_WORDS]
    return " ".join(x)


def remove_word_transformer(ser):
    return ser.apply(remove_words)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def strip_html_transformer(ser):
    return ser.apply(strip_tags)
