import pytest
import pandas as pd

from transformers import (
    compound_word_transformer,
    spacy_lemmatize_transformer,
    strip_html_transformer,
    remove_word_transformer,
    remove_word_and_underscore_transformer,
)

COMPLEX_TITLES = [
    ("Bestandszahlen Fahrzeugzulassungen (KFZ) 2018", "bestandszahlen fahrzeugzulassungen kfz"),
    ("Bombenfunde in Düsseldorf seit 1995", "bombenfunde"),
    ("Stadt Moers: Müll", "müll"),
    ("Adressen_StadtAachen", "adresse"),
    ("Bedarfsgemeinschaften, Leistungsempfänger*innen und Leistungen nach SGB II seit 2005", "bedarfsgemeinschaften leistung sgb ii"),
    ("Arbeitsmarktstatistik Arbeitslose (Gelsenkirchen)", "arbeitsmarktstatistik arbeitslose"),
    ("Rhein-Kreis Neuss: 2019 Arbeitsmarkt im Überblick", "arbeitsmarkt überblick"),
    #("", ""),
]


def test_compound_transformer():
    x = pd.DataFrame.from_dict({"TEST": ["Abfallwirtschaft"]})
    result = compound_word_transformer(x["TEST"])
    assert result.iloc[0] == "Abfallwirtschaft Abfall Wirtschaft"


def test_spacy_lemmatize_transformer():
    x = pd.DataFrame.from_dict({"TEST": ["  TEXT WITH NUMBERS 123, Puncts ?*- and space    "]})
    result = spacy_lemmatize_transformer(x["TEST"])
    assert result.iloc[0] == "text with numbers puncts and space"


def test_strip_html_transformer():
    x = pd.DataFrame.from_dict({"TEST": ["<br><p>TEXT WITH <b>HTML</b> TAG</p>"]})
    result = strip_html_transformer(x["TEST"])
    assert result.iloc[0] == "TEXT WITH HTML TAG"


def test_remove_word_transformer():
    x = pd.DataFrame.from_dict({"TEST": ["TEXT dezember WITH hanse REMOVE WORDS: Köln"]})
    result = remove_word_transformer(x["TEST"])
    assert result.iloc[0] == "TEXT WITH REMOVE WORDS:"


@pytest.mark.parametrize("test_input,expected", COMPLEX_TITLES)
def test_remove_word_complex(test_input, expected):
    x = pd.DataFrame.from_dict({"TEST": [test_input]})
    # This is how our pipeline works
    result = remove_word_and_underscore_transformer(x["TEST"])
    result = spacy_lemmatize_transformer(result)
    result = remove_word_transformer(result)
    assert result.iloc[0] == expected


