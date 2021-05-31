import proof
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

from skpipelines import model_pipeline

TF_COS_COLUMNS = ['dct:title', 'dcat:theme']
TFIDF_COLUMNS = ['dct:description']

def load_data(data):
    # Load the data
    data['table'] = pd.read_csv('training.csv')

def remove_empty_musterdaten(data):
    # Select relevant rows from the table
    data['table'] = data['table'].dropna(subset=["MUSTERDATENSATZ"])

def fill_na(data):
    # Fill NaN values in feature columns
    data['features'] = data['features'].fillna("")

def select_columns(data):
    data['features'] = data['table'][TF_COS_COLUMNS + TFIDF_COLUMNS]
    data['labels'] = data['table']['MUSTERDATENSATZ']

def split_test_training(data):
    X_train, X_test, y_train, y_test = train_test_split(data['features'], data['labels'], test_size=0.2, random_state=42)

    data['features_train'] = X_train
    data['features_test'] = X_test
    data['labels_train'] = y_train
    data['labels_test'] = y_test

@proof.never_cache
def train(data):
    model_pipeline.fit(data['features_train'], data['labels_train'])
    y_pred = model_pipeline.predict(data['features_test'])
    score = accuracy_score(data['labels_test'], y_pred)
    print(f"Accuracy score: {score}")

def prepare(pipeline):
    cleaned_data = pipeline.then(remove_empty_musterdaten)
    selected_columns = cleaned_data.then(select_columns)
    fill = selected_columns.then(fill_na)
    test_training = fill.then(split_test_training)
    return test_training

def cross_validation(data):
    parameters = {
        #'preprocessing__desc__vect__max_df': (0.5, 0.75, 1.0),
        #'preprocessing__desc__vect__max_features': (None, 5000, 10000, 50000),
        #'preprocessing__desc__vect__ngram_range': ((1,3), (1,4)),  # unigrams or bigrams
        #'preprocessing__desc__vect__ngram_range': ((1, 1), (1, 2), (1,3)),  # unigrams or bigrams
        #'preprocessing__title__vect__max_df': (0.5, 0.75, 1.0),
        # 'vect__max_features': (None, 5000, 10000, 50000),
        #'vect__ngram_range': ((1, 1), (1, 2), (1,3)),  # unigrams or bigrams
        #'preprocessing__desc__tfidf__norm': ('l1', 'l2'),
        #'preprocessing__desc__tfidf__smooth_idf': (True, False),
        #'preprocessing__desc__tfidf__sublinear_tf': (True, False),
        #'preprocessing__desc__tfidf__use_idf': (True, False),
        #'preprocessing__title__tfidf__use_idf': (True, False),
        #'preprocessing__title__tfidf__norm': ('l1', 'l2'),
        #'preprocessing__title__tfidf__smooth_idf': (True, False),
        #'preprocessing__title__tfidf__sublinear_tf': (True, False),
        #'preprocessing__title__tfidf__ngram_range': ((1, 1), (1, 2), (1,3)),
        #'preprocessing__title__tfidf__max_df': (0.1, 0.2, 0.3, 0.4, 0.5),
        #'preprocessing__title__tfidf__min_df': (0.0, 0.5, 0.75, 1.0),
        #'preprocessing__title__tfidf__binary': (True, False),
        #'preprocessing__title__tfidf__': (True, False),
        #'preprocessing__title__tfidf__': (True, False),
        #'preprocessing__theme__vect__max_features': (None, 5000, 10000, 50000),
        #'preprocessing__theme__vect__ngram_range': ((1, 1), (1, 2), (1,3)),  # unigrams or bigrams
        #'preprocessing__theme__tfidf__norm': ('l1', 'l2'),
        #'preprocessing__theme__tfidf__binary': (True, False),
        #'preprocessing__theme__tfidf__smooth_idf': (True, False),
        #'preprocessing__theme__tfidf__sublinear_tf': (True, False),
        #'preprocessing__theme__tfidf__use_idf': (True, False),
    }
    grid_search = GridSearchCV(model_pipeline, parameters, n_jobs=-1, verbose=1)
    grid_search.fit(data['features_train'], data['labels_train'])
    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
            print("\t%s: %r" % (param_name, best_parameters[param_name]))

def run_cv(data_pipeline, pipeline):
    cv = pipeline.then(cross_validation)
    data_pipeline.run()

def save_train(data_pipeline, pipeline):
    pipeline.then(train)

    data_pipeline.run()

def main():
    data_pipeline = proof.Analysis(load_data)
    pipeline = prepare(data_pipeline)
    save_train(data_pipeline,pipeline)
    #run_cv(main,pipeline)

if __name__ == "__main__":
    main()
