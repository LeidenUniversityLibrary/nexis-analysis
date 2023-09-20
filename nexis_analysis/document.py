# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Representation of Nexis Uni documents"""
import datetime
from . import extract
import pathlib
from typing import Union

class NexisDocument(object):
    """A document with typical properties"""

    def __init__(self, raw_source: str):
        """Create a NexisDocument from GFM text"""
        self.raw_source = raw_source

    @property
    def body(self) -> str:
        return extract.get_body(self.raw_source)

    @property
    def title(self) -> str:
        return extract.get_title(self.raw_source)

    @property
    def length(self) -> int:
        return extract.get_length(self.raw_source)

    @property
    def date(self) -> datetime.datetime:
        return extract.get_date(self.raw_source)

    @property
    def date_str(self) -> str:
        return extract.get_date_str(self.raw_source)


def doc_from_file(file_name: Union[str, pathlib.Path]) -> NexisDocument:
    """Create a NexisDocument by loading a GFM file"""
    with open(file_name, "r", encoding="utf-8") as fh:
        raw_source = fh.read()
    return NexisDocument(raw_source)
