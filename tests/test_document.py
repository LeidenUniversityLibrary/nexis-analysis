# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Test that metadata are correctly extracted from documents"""
from collections import Counter
from nexis_analysis import document
import pathlib
import pytest

def get_path(relative_path):
    return pathlib.Path("tests/fixtures", relative_path).resolve()

@pytest.fixture()
def text():
    yield "This is a piece of text."

def test_document_init(text):
    doc = document.NexisDocument(text)

    assert doc.raw_source == text
    assert doc.body is not None
    assert doc.length is None
    assert doc.title is None
    assert doc.date is None
    assert doc.date_str is None
    assert doc.byline is None
    assert doc.section is None
    assert doc.publication is None
    assert doc.search_terms_in_body_counts() == Counter()
    assert doc.title_or_incipit == text
    assert text in str(doc)
    assert doc.as_dict()

def test_doc_from_file():
    doc = document.doc_from_file(get_path("test1.md"))
    assert doc.body is not None
    assert doc.length is not None
    assert doc.title is not None
    assert doc.date is not None
    assert doc.date_str is not None
    assert doc.byline is not None
    assert doc.section is not None
    assert doc.publication is not None
    assert len(doc.search_terms_in_body_counts()) == 1
    assert doc.title_or_incipit == doc.title

def test_empty_doc():
    text = ""
    doc = document.NexisDocument(text)

    assert doc.raw_source == text
    assert doc.body is not None
    assert doc.length is None
    assert doc.title is None
    assert doc.date is None
    assert doc.date_str is None
    assert doc.byline is None
    assert doc.section is None
    assert doc.publication is None
    assert doc.search_terms_in_body_counts() == Counter()
    assert doc.search_terms_in_body_counts_lower() == Counter()
    assert doc.title_or_incipit == "[No title or body]"
    assert "[No title or body]" in str(doc)
