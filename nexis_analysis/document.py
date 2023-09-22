# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Representation of Nexis Uni documents"""
from collections import Counter
import datetime
from . import extract
import pathlib
from textwrap import dedent, shorten
from typing import Union

class NexisDocument(object):
    """A document with typical properties"""

    def __init__(self, raw_source: str):
        """Create a NexisDocument from GFM text"""
        self.raw_source = raw_source

    def __str__(self):
        result = """\
        {}
        ---""".format(self.title_or_incipit)
        return dedent(result)

    @property
    def body(self) -> str:
        return extract.get_body(self.raw_source)

    @property
    def title(self) -> str:
        return extract.get_title(self.raw_source)

    @property
    def title_or_incipit(self) -> str:
        if self.title:
            return self.title
        elif self.body:
            return shorten(self.body, width=60)
        else:
            return "[No title or body]"

    @property
    def length(self) -> int:
        return extract.get_length(self.raw_source)

    @property
    def date(self) -> datetime.datetime:
        return extract.get_date(self.raw_source)

    @property
    def load_date(self) -> datetime.datetime:
        return extract.get_load_date(self.raw_source)

    @property
    def date_str(self) -> str:
        return extract.get_date_str(self.raw_source)

    @property
    def byline(self) -> str:
        return extract.get_byline(self.raw_source)

    @property
    def section(self) -> str:
        return extract.get_section(self.raw_source)

    @property
    def publication(self) -> str:
        return extract.get_publication(self.raw_source)

    def search_terms_in_body_counts(self) -> Counter:
        return extract.get_search_terms_count(self.raw_source)

    def search_terms_in_body_counts_lower(self) -> Counter:
        return extract.get_search_terms_count(self.raw_source, False)

    def as_dict(self) -> dict:
        return {
            "title": self.title_or_incipit,
            "publication": self.publication if self.publication else "[no publication]",
            "date": self.date.isoformat() if self.date else "[no date]",
            "load_date": self.load_date.isoformat() if self.load_date else "[no date]",
            "section": self.section if self.section else "[no section]",
            "byline": self.byline if self.byline else "[no byline]",
            "length": self.length if self.length else "[no length]",
        }


def doc_from_file(file_name: Union[str, pathlib.Path]) -> NexisDocument:
    """Create a NexisDocument by loading a GFM file"""
    with open(file_name, "r", encoding="utf-8") as fh:
        raw_source = fh.read()
    return NexisDocument(raw_source)
