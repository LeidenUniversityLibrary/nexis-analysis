# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Test that metadata are correctly extracted from documents"""
from collections import Counter
import datetime
from nexis_analysis import extract
import pathlib
import pytest

def get_path(relative_path):
    return pathlib.Path("tests/fixtures", relative_path).resolve()

def load_doc(path: str) -> str:
    return get_path(path).read_text(encoding="utf-8")

@pytest.fixture(params=["test1.md", "test2.md"])
def doc(request):
    yield load_doc(request.param)

def test_get_body(doc):
    body = extract.get_body(doc)
    assert body
    assert "**Body**" not in body
    assert "**Load-Date**" not in body


@pytest.mark.parametrize(
    "document,title",
    [
        (load_doc("test1.md"), "Veldslag om smartphone als mobiele bank"),
        (load_doc("test2.md"), "Schaduwbankieren valt mee, vindt Nederlandsche Bank"),
        ("# [***<u>Stresstest</u>***](https://advance.lexis.com/api/document?collection=news&id=urn:contentItem:601X-HCR1-JC5G-10P8-00000-00&context=1516831) [***<u>CPB: coronacrisis kan financiële sector schaden</u>***](https://advance.lexis.com/api/document?collection=news&id=urn:contentItem:601X-HCR1-JC5G-10P8-00000-00&context=1516831)", "Stresstest CPB: coronacrisis kan financiële sector schaden"),
    ]
)
def test_get_title(document, title):
    doc_title = extract.get_title(document)
    assert doc_title
    assert "**" not in doc_title
    assert doc_title == title

@pytest.mark.parametrize(
    "document,length",
    [
        (load_doc("test1.md"), 952),
        (load_doc("test2.md"), 245),
    ]
)
def test_get_length(document, length):
    doc_length = extract.get_length(document)
    assert doc_length
    assert isinstance(doc_length, int)
    assert doc_length == length

@pytest.mark.parametrize(
    "document,date",
    [
        (load_doc("test1.md"), datetime.datetime(2017, 10, 4)),
        (load_doc("test2.md"), datetime.datetime(2012, 11, 30)),
        ("August 5, 2022 6:43 PM GMT", datetime.datetime(2022, 8, 5)),
        ("6 april 2012", datetime.datetime(2012, 4, 6)),
        ("Het Parool\n\nNovember 3, 2000", datetime.datetime(2000, 11, 3)),
        ("(+31) 34 379 9909", None),
        ("**Section:** Financieel: Scorpio; N.1 van 2006, J.9; P.41; fdw", None),
        ("Nov 23, 2023", None),
    ]
)
def test_get_date(document, date):
    if date is None:
        assert extract.get_date(document) is None
    else:
        assert extract.get_date(document) == date

@pytest.mark.parametrize(
    "document,date",
    [
        (load_doc("test1.md"), datetime.datetime(2017, 10, 3)),
        (load_doc("test2.md"), datetime.datetime(2012, 11, 30)),
        ("August 5, 2022 6:43 PM GMT", None),
        ("**Load-Date:** Apr 6, 2012", None),
        ("**Load-Date:** November 3, 2000", datetime.datetime(2000, 11, 3)),
        ("(+31) 34 379 9909", None),
        ("**Section:** Financieel: Scorpio; N.1 van 2006, J.9; P.41; fdw", None),
        ("Nov 23, 2023", None),
    ]
)
def test_get_load_date(document, date):
    if date is None:
        assert extract.get_load_date(document) is None
    else:
        assert extract.get_load_date(document) == date

@pytest.mark.parametrize(
    "document,date_str",
    [
        (load_doc("test1.md"), "4 oktober 2017 woensdag"),
        (load_doc("test2.md"), "30 november 2012 vrijdag"),
        ("augustus 5, 2022 6:43 PM GMT", "augustus 5, 2022"),
    ]
)
def test_get_date_str(document, date_str):
    assert extract.get_date_str(document) == date_str

@pytest.mark.parametrize(
    "document,byline",
    [
        (load_doc("test1.md"), "DOOR MARC VAN DEN EERENBEEMT"),
        (load_doc("test2.md"), None),
    ]
)
def test_get_byline(document, byline):
    if byline is None:
        assert extract.get_byline(document) is None
    else:
        assert extract.get_byline(document) == byline

@pytest.mark.parametrize(
    "document,section",
    [
        (load_doc("test1.md"), "Economie; Blz. 28, 29"),
        (load_doc("test2.md"), None),
    ]
)
def test_get_section(document, section):
    if section is None:
        assert extract.get_section(document) is None
    else:
        assert extract.get_section(document) == section

@pytest.mark.parametrize(
    "document,publication",
    [
        (load_doc("test1.md"), "de Volkskrant"),
        (load_doc("test2.md"), "De Gooi- en Eemlander"),
        ("No publication here", None),
    ]
)
def test_get_publication(document, publication):
    if publication is None:
        assert extract.get_publication(document) is None
    else:
        assert extract.get_publication(document) == publication

@pytest.mark.parametrize(
    "document,counts",
    [
        ("***<u>mijn KEYword</u>***", Counter({'mijn KEYword': 1})),
        (load_doc("test1.md"), Counter({'niet-bancaire': 1})),
        (load_doc("test2.md"), Counter({'Schaduwbanken': 1, 'Schaduwbankieren': 1, 'schaduwbank': 1, 'schaduwbanken': 1, 'schaduwbankieren': 2,})),
    ]
)
def test_term_in_body_counts(document, counts):
    assert extract.get_search_terms_count(document) == counts

@pytest.mark.parametrize(
    "document,counts",
    [
        ("***<u>mijn KEYword</u>***", Counter({'mijn keyword': 1})),
        (load_doc("test1.md"), Counter({'niet-bancaire': 1})),
        (load_doc("test2.md"), Counter({'schaduwbank': 1, 'schaduwbanken': 2, 'schaduwbankieren': 3,})),
    ]
)
def test_term_in_body_counts_lower(document, counts):
    assert extract.get_search_terms_count(document, False) == counts
