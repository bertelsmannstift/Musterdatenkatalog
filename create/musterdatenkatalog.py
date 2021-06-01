import pandas as pd
import requests
import csv

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

MD_CACHE = {}
CITY_CACHE = {}
MD_API = "https://daten.musterdatenkatalog.de/api"

MDK_COLUMNS = [ "dct:title", "dct:identifier", "dcat:landingpage", "dct:description", "ORG", "dcat:Distribution.dct:license", "dcat:theme", "updated_at", "added", "MUSTERDATENSATZ", "THEMA", "BEZEICHNUNG",]

RAW_RESULT_MDK_COLUMNS = [ "dct:title", "dct:identifier", "dcat:landingpage", "dct:description_bkp", "distribution", "ORG", "dcat:Distribution.dct:license", "dcat:theme", "tags", "updated_at", "added", "dct:description", "MUSTERDATENSATZ"]


def get_city_name(city):
    '''
    if the city is in the CITY_CACHE which was filled from cities that have different names in the NRW Musterdatenkatalog we return that name otherwise the default
    '''
    return CITY_CACHE.get(city, city)

def get_m(find_from, dataset_id, city, default):
    '''
    find Musterdatensatz from different data by id and city
    used to merge with NRW MDK
    if the dataset can't be find (probably a new dataset) we use the score form the ML modell
    '''
    city = get_city_name(city)
    result = find_from.loc[(find_from["dct:identifier"]==dataset_id) & (find_from["ORG"]==city)]
    try:
        if len(result) == 1:
            return result["MUSTERDATENSATZ"].values[0]
    except:
        logging.error("can't get Musterdatensazz for city %s and id %s" , city, dataset_id)
    return default

def merge_data(merge_into, merge_from):
    '''
    find dataset by id and city; change modeldataset on MDK D
    '''
    merge_into["MUSTERDATENSATZ"] = merge_into.apply(lambda x : get_m(merge_from, x["dct:identifier"],x["ORG"], x["MUSTERDATENSATZ"]), axis=1)
    return merge_into

def musterdaten(musterdatensatz):
    return MD_CACHE[musterdatensatz]


def get_thema(musterdatensatz):
    return musterdaten(musterdatensatz)["thema"]


def get_bezeichnung(musterdatensatz):
    return musterdaten(musterdatensatz)["bezeichnung"]


def set_cache(musterdatensatz, thema, bezeichnung):
    MD_CACHE[musterdatensatz] = { "thema": thema, "bezeichnung": bezeichnung }


def save_musterdatenfrom_api(force=False):
    if len(MD_CACHE) < 1 or force:
        resp = requests.get(f"{MD_API}/modeldataset?per_page=1000")
        data = resp.json()
        [set_cache(d["name"], d["modelsubject"]["title"], d["title"]) for d in data["data"]]


def set_thema_bezeichnung(data):
    '''
    set thema and bezeichung for data based on Musterdatensatz
    '''
    data["THEMA"] = data.apply(lambda x : get_thema(x["MUSTERDATENSATZ"]), axis=1)
    data["BEZEICHNUNG"] = data.apply(lambda x : get_bezeichnung(x["MUSTERDATENSATZ"]), axis=1)

    return data

def collect_different_city_names(filename):
    '''
    some cities have different names in the NRW dataset than how they are named in govdata, we need to harmonize those
    '''
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            CITY_CACHE[row["ORG_NEW"]] = row["ORG"]

def merge_nrw_into_data(data):
    '''
    we merge the previous Musterdatenkatalog from NRW (Version 2.2) into the resulting Musterdatenkatalog form the ML predictions. NRW was scored manually, so we don't want to lose that verified scoring.
    '''
    collect_different_city_names("changed_city_name.csv")
    nrw = pd.read_csv("nrw_2_2_1.csv")

    modified_data = merge_data(data, nrw)
    return modified_data

def main():
    mdk = pd.read_csv("mdk_predicted_result_20210301.csv")
    mdk.columns = RAW_RESULT_MDK_COLUMNS

    logging.info("merge nrw and D")

    merged_data = merge_nrw_into_data(mdk)

    save_musterdatenfrom_api()

    logging.info("set thema and bezeichnung")
    data = set_thema_bezeichnung(merged_data)

    # only select columns we want
    end_result = data[MDK_COLUMNS]

    # write endresult to csv ( don't add new index column )
    end_result.to_csv("musterdatenkatalog_deutschland.csv", index=False)


if __name__ == "__main__":
    args = sys.argv[1:]
    main()
