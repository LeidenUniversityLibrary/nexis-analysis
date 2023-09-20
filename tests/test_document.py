# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Test that metadata are correctly extracted from documents"""

from nexis_analysis import document, extract
import pytest

@pytest.fixture()
def text():
    yield "This is a piece of text."

def test_document_init(text):
    doc = document.NexisDocument(text)

    assert doc.raw_source == text
    assert doc.body is None
    assert doc.length is None
    assert doc.title is None
    assert doc.date is None
    assert doc.date_str is None
