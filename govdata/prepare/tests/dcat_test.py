import pytest
import pandas
from bs4 import BeautifulSoup

from dcat import DCATRDF, soup_find_tree, External

@pytest.fixture
def data(request):
    simple = open(f"tests/fixtures/{request.param}.rdf", "r")
    return simple.read()


@pytest.fixture
def cities():
    return pandas.read_csv("tests/fixtures/cities.csv")


@pytest.fixture
def categories():
    return {
            "http://publications.europa.eu/resource/authority/data-theme/TRAN": "Verkehr",
            "http://publications.europa.eu/resource/authority/data-theme/ECON": "Wirtschaft"
            }


@pytest.mark.parametrize('data', ( 'simple', 'different', ), indirect=True)
class TestDCATAP:

    def test_title(self, data, cities):
        d = DCATRDF(data, cities)

        assert d.get_title() == "Dataset Title"

    def test_id(self, data, cities):
        d = DCATRDF(data, cities)

        assert d.get_id() == "12345"

    def test_description(self, data, cities):
        d = DCATRDF(data, cities)

        assert d.get_description() == "Description"

    def test_license(self, data, cities):
        d = DCATRDF(data, cities)

        assert d.get_license() == "license"

    def test_url(self, data, cities):
        d = DCATRDF(data, cities)

        assert d.get_url() == "url"

    def test_city(self, data, cities):
        d = DCATRDF(data, cities)

        assert d.get_city() == "Altenahr"

    def test_updated_at(self, data, cities):
        d = DCATRDF(data, cities)

        assert d.get_updated_at() == "2021-02-10"

    def test_categories(self, data, cities, categories):
        d = DCATRDF(data, cities, categories)

        assert d.get_categories() == "Verkehr, Wirtschaft"

    def test_tags(self, data, cities):
        d = DCATRDF(data, cities)

        assert d.get_tags() == "bebauungsplan, bauleitplan"

    def test_distribution_description(self, data, cities):
        d = DCATRDF(data, cities)

        assert d.get_distribution_description() == "Distribution Description, Distribution Description"


class TestExternal:
    def test_find(self):
        e = External("http://publications.europa.eu/resource/authority/data-theme/GOVE")
        assert e.find('skos:prefLabel', { "xml:lang":"de"}).text == "Regierung und öffentlicher Sektor"

    def test_find_text(self):
        e = External("http://publications.europa.eu/resource/authority/data-theme/GOVE")
        assert e.find_text('skos:prefLabel', { "xml:lang":"de"}) == "Regierung und öffentlicher Sektor"


@pytest.mark.parametrize('data', ( 'simple', ), indirect=True)
def test_soup_find_tree(data):
    soup = BeautifulSoup(data, 'lxml')
    assert soup_find_tree(soup, ['dct:creator', 'foaf:name']).text == "Verbandsgemeinde Altenahr"


@pytest.mark.parametrize('data', ( 'simple', ), indirect=True)
def test_soup_find_tree(data):
    soup = BeautifulSoup(data, 'lxml')
    assert soup_find_tree(soup, ['vcard:fn']).text == "Verbandsgemeinde Altenahr"

