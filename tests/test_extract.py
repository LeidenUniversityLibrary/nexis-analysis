# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Test that metadata are correctly extracted from documents"""
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


@pytest.mark.parametrize(
    "document,title",
    [
        (load_doc("test1.md"), "Veldslag om smartphone als mobiele bank"),
        (load_doc("test2.md"), "Schaduwbankieren valt mee, vindt Nederlandsche Bank"),
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
    ]
)
def test_get_date(document, date):
    assert extract.get_date(document) == date

@pytest.mark.parametrize(
    "document,date_str",
    [
        (load_doc("test1.md"), "4 oktober 2017 woensdag"),
        (load_doc("test2.md"), "30 november 2012 vrijdag"),
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
