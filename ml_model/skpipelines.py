from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler

from transformers import (
    compound_word_transformer,
    spacy_lemmatize_transformer,
    strip_html_transformer,
    remove_word_transformer,
    remove_word_and_underscore_transformer,
)

tf_cos_pipe = Pipeline([
    ('remove_word_and_underscore', FunctionTransformer(remove_word_and_underscore_transformer, validate=False)),
    ('text', FunctionTransformer(compound_word_transformer, validate=False)),
    ('lemma', FunctionTransformer(spacy_lemmatize_transformer, validate=False)),
    ('remove_words', FunctionTransformer(remove_word_transformer, validate=False)),
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer(use_idf=True, norm='l2', sublinear_tf=True)),
])

tf_desc = Pipeline([
    ('remove_word_and_underscore', FunctionTransformer(remove_word_and_underscore_transformer, validate=False)),
    ('text', FunctionTransformer(compound_word_transformer, validate=False)),
    ('lemma', FunctionTransformer(spacy_lemmatize_transformer, validate=False)),
    ('remove_words', FunctionTransformer(remove_word_transformer, validate=False)),
    ('strip_html', FunctionTransformer(strip_html_transformer, validate=False)),
    ('vect', CountVectorizer(ngram_range=(1, 3), max_df=0.5, max_features=10000)),
    ('tfidf', TfidfTransformer(norm='l2', use_idf=True, sublinear_tf=True, smooth_idf=True)),
])

title_pipeline = Pipeline([
    ('remove_word_and_underscore', FunctionTransformer(remove_word_and_underscore_transformer, validate=False)),
    ('text', FunctionTransformer(compound_word_transformer, validate=False)),
    ('lemma', FunctionTransformer(spacy_lemmatize_transformer, validate=False)),
    ('remove_words', FunctionTransformer(remove_word_transformer, validate=False)),
    ('tfidf', TfidfVectorizer(norm='l2', smooth_idf=True, sublinear_tf=False, use_idf=True, max_df=0.5, min_df=0.0)),
])

preprocessing = ColumnTransformer(
    transformers=[
        ("title", title_pipeline, 'dct:title'),
        ("theme", tf_cos_pipe, 'dcat:theme'),
        ("desc", tf_desc, 'dct:description'),
    ],
    transformer_weights={
        'title': 1.0,
        'theme': 0.4,
        'desc': 0.4,
    },
    n_jobs=-1,
)

model_pipeline = Pipeline(steps=[
    ('preprocessing', preprocessing),
    ('skaling', RobustScaler(with_centering=False)),
    ('classifier', KNeighborsClassifier(n_neighbors=5, n_jobs=-1,))
])
