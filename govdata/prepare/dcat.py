from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse
from datetime import datetime
import requests
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

class MyTag(Tag):
    def find_tree(self, element_tree, *kwargs):
        result = self.find(element_tree.pop(0))
        if len(element_tree) >0:
            for el in element_tree:
                result = result.find(el)
        return result

    def find_all_with_parent(self, element, parent, *kwargs):
        results = self.find_all(element, kwargs)
        return [result for result in results if result.parent.name == parent]

    def find_with_parent(self, element, parent, *kwargs):
        results = self.find_all(element, kwargs)
        for result in results:
            if result.parent.name == parent:
                return result
        return None

class DCATRDF:
    def __init__(self, contents, cities, categories = []):
        self.soup = BeautifulSoup(contents, 'lxml', element_classes={Tag: MyTag})
        self.df = cities
        self.categories = categories

    def get_data(self):
        return {
                'dct:title': self.get_title(),
                'dct:identifier': self.get_id(),
                'url': self.get_url(),
                'dct:description': self.get_description(),
                'distribution_description': self.get_distribution_description(),
                'city': self.get_city(),
                'license': self.get_license(),
                'categories': self.get_categories(),
                'tags': self.get_tags(),
                'updated_at': self.get_updated_at(),
                'added': datetime.strftime(datetime.now(), "%Y-%m-%d")
                }

    def get_title(self):
        try:
            return self.soup.find('dcat:dataset').find_with_parent('dct:title', 'dcat:dataset').text
        except:
            return ""

    def get_license(self):
        try:
            return self.soup.find('dct:license').get('rdf:resource')
        except:
            return ""

    def get_category(self, url):
        return self.categories.get(url, "")

    def get_categories(self):
        try:
            categories = self.soup.find_all('dcat:theme')
            return ", ".join([self.get_category(c.get('rdf:resource')) for c in categories])
        except:
            logging.info("failure")
            return ""

    def get_tags(self):
        try:
            tags = self.soup.find_all('dcat:keyword')
            return ", ".join([t.text for t in tags])
        except:
            logging.info("failure")
            return ""

    def get_url(self):
        try:
            return self.soup.find('dcat:dataset').get('rdf:about')
        except:
            return ""

    def get_id(self):
        try:
            return self.soup.find('dct:identifier').text
        except:
            return ""

    def get_description(self):
        try:
            return self.soup.find('dcat:dataset').find_with_parent('dct:description', 'dcat:dataset').text
        except:
            return ""

    def get_distribution_description(self):
        try:
            return ", ".join([t.text for t in self.soup.find('dcat:dataset').find_all_with_parent('dct:description', 'dcat:distribution')])
        except:
            return ""

    def get_updated_at(self):
        try:
            text = self.soup.find('dct:modified').text
            return datetime.strftime(parse(text), "%Y-%m-%d")
        except:
            return ""

    def get_city(self):
        columns = [['vcard:fn'], ['dct:publisher', 'foaf:name'], ['dcatde:maintainer', 'foaf:name'], ['dct:maintainer', 'foaf:name'], ['dct:creator', 'foaf:name']]
        for col_tree in columns:
            try:
                tag = self.soup.find('dcat:dataset').find_tree(col_tree)
                stelle = tag.text
                if self.df["Value"].str.contains(stelle).any():
                    row = self.df.loc[self.df["Value"] == stelle, "Kommune"]
                    return row.array[0]
                else:
                    logging.debug("not in csv:", stelle)
            except Exception as e:
                logging.info("not this one")
                continue
        return ""

    def get_matching_row(self, column, text):
        try:
            if self.df[column].str.contains(text).any():
                return self.df.loc[self.df[column]==text, "Kommune"]
        except:
            return ""


def soup_find_tree(soup, tree):
    result = soup.find(tree.pop(0))
    for el in tree:
        result = result.find(el)
    return result


class External:

    def __init__(self, url):
        page = requests.get(url)
        self.soup = BeautifulSoup(page.text, 'xml')

    def find(self, tag, attr):
        return self.soup.find(tag, attr)

    def find_text(self, tag, attr):
        try:
            return self.find(tag, attr).text
        except:
            return ""

    def find_all(self, tag):
        return self.soup.find_all(tag)

