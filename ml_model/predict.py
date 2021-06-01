import pickle
from datetime import datetime
import pandas as pd

TITLE_COLUMNS = ['dct:title']
THEME_COLUMNS = ['dcat:theme']
DESCRIPTION_COLUMNS = ['dct:description']

COLUMNS = TITLE_COLUMNS + THEME_COLUMNS + DESCRIPTION_COLUMNS

def load_model(model_file):
    infile = open(model_file, "rb")
    model = pickle.load(infile)
    infile.close()
    return model

def prepare_data(raw_data):
    data = raw_data[COLUMNS]
    data.fillna("", inplace=True)
    return data


def probability(filename, model_file):
    '''
    save probabilties as well for crowdsourcing tool
    '''
    raw_data = pd.read_csv(filename, dtype=str)
    model = load_model(model_file)
    data = prepare_data(raw_data)
    proba = model.predict_proba(data)

    #save probabilities
    probablilty_result_filename = f"mdk_predicted_probability_result_{datetime.now().strftime('%Y%m%d')}.csv"
    outfile = open(probablilty_result_filename, "wb")
    pickle.dump(proba, outfile)
    outfile.close()


def predict(filename, model_file):
    raw_data = pd.read_csv(filename, dtype=str)
    raw_data["dct:description_bkp"] = raw_data['dct:description'].map(str)
    raw_data["dct:description"] = raw_data['dct:description'].map(str) + ',' + raw_data['tags'].map(str)
    model = load_model(model_file)
    data = prepare_data(raw_data)
    result = model.predict(data)
    raw_data["MUSTERDATENSATZ"] = result

    result_filename = f"/mdk_predicted_result_{datetime.now().strftime('%Y%m%d')}.csv"
    raw_data.to_csv(result_filename, index=False)

def main():
    model_filename = "model.pickle"
    predict("govdata/results.csv", model_filename)

if __name__ == "__main__":
    main()


