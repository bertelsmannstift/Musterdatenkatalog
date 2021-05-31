import pandas
import os
import csv
import logging

from pathlib import Path
from datetime import datetime
from tqdm import tqdm

from dcat import DCATRDF, MyTag, External


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')


def categorize(contents, cities, categories):
    """
    find dataset title, city, id, url, license, category, decription, updated_at, today
    """
    try:
        dataset = DCATRDF(contents, cities, categories)
        if dataset.get_city() != "":
            return dataset.get_data()
    except:
        logging.debug('unable to parse city')
        return {"error": "unable to parse"}


def collect_categories():
    EU_CATEGORIES = {}
    url = "https://publications.europa.eu/resource/authority/data-theme"
    categories = External(url).find_all('rdf:Description')
    for c in categories:
        url = c.get("rdf:about")
        if not EU_CATEGORIES.get(url):
            category = External(url).find_text('skos:prefLabel', { "xml:lang":"de"})
            EU_CATEGORIES[url] = category
    return EU_CATEGORIES


def start(input_dir, cities_csv):
    categories = collect_categories()
    cities = pandas.read_csv(cities_csv)
    fieldnames = ['dct:title', 'dct:identifier', 'url', 'dct:description', 'distribution_description', 'city', 'license', 'categories', 'tags', 'updated_at', 'added']
    writer = csv.DictWriter(open(f"results_{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv",mode="w"), fieldnames=fieldnames)
    writer.writeheader()
    for filename in tqdm(os.listdir(input_dir)):
        if Path(filename).suffix != ".rdf":
            continue
        with open(f'{input_dir}/{filename}') as f:
            contents = f.read()
            data = categorize(contents,cities, categories)
            if "error" not in data:
                writer.writerow(data)

    logging.debug('finish processing')


def main():
    start("fixtures", "cities.csv")


if __name__ == "__main__":
    main()
