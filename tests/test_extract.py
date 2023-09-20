# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Test that metadata are correctly extracted from documents"""
import datetime
from nexis_analysis import document
import pathlib
import pytest

def load_doc(path):
    return document.NexisDocument(str(pathlib.Path("tests/fixtures", path).resolve()))

@pytest.fixture(params=["test1.md", "test2.md"])
def doc(request):
    yield load_doc(request.param)


def test_body(doc):
    assert doc.body
    assert "**Body**" not in doc.body

@pytest.mark.parametrize(
    "document,title",
    [
        (load_doc("test1.md"), "Veldslag om smartphone als mobiele bank"),
        (load_doc("test2.md"), "Schaduwbankieren valt mee, vindt Nederlandsche Bank"),
    ]
)
def test_title(document, title):
    assert document.title
    assert "**" not in document.title
    assert document.title == title

@pytest.mark.parametrize(
    "document,length",
    [
        (load_doc("test1.md"), 952),
        (load_doc("test2.md"), 245),
    ]
)
def test_length(document, length):
    assert document.length
    assert isinstance(document.length, int)
    assert document.length == length

@pytest.mark.parametrize(
    "document,date_str,date",
    [
        (load_doc("test1.md"), "4 oktober 2017 woensdag", datetime.datetime(2017, 10, 4)),
        (load_doc("test2.md"), "30 november 2012 vrijdag", datetime.datetime(2012, 11, 30)),
    ]
)
def test_date(document, date_str, date):
    assert document.date == date
    assert document.date_str == date_str
