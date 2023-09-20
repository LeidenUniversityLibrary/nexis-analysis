# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Extract information from documents"""
import datetime
from . import document
import pathlib
import re
from typing import Union

month_by_name = {
    "januari": 1,
    "februari": 2,
    "maart": 3,
    "april": 4,
    "mei": 5,
    "juni": 6,
    "juli": 7,
    "augustus": 8,
    "september": 9,
    "oktober": 10,
    "november": 11,
    "december": 12,
}



def doc_from_file(file_name: Union[str, pathlib.Path]) -> document.NexisDocument:
    """Create a NexisDocument by loading a GFM file"""
    with open(file_name, "r", encoding="utf-8") as fh:
        raw_source = fh.read()
    doc = document.NexisDocument(raw_source)
    doc.body = get_body(raw_source)
    doc.title = get_title(raw_source)
    doc.date = get_date(raw_source)
    doc.date_str = get_date_str(raw_source)
    doc.length = get_length(raw_source)
    return doc


def get_body(raw_source):

    body_start = """**Body**"""
    body_start_index = raw_source.index(body_start) + len(body_start)
    body_end = """**Load-Date:**"""
    body_end_index = raw_source.index(body_end)
    return raw_source[body_start_index:body_end_index].strip()


def get_title(raw_source):
    title = re.search(r"# \[\*{3}<u>(.+)</u>\*{3}\]", raw_source)
    if title:
        return title.group(1).replace("</u>*** ***<u>", " ")


def get_length(raw_source):
    length = re.search(r"\*\*Length:\*\*\s(\d+)\swords", raw_source)
    if length:
        return int(length.group(1))


def get_date(raw_source):
    date = re.search(r"(\d\d?) (\w+) (\d{4}) \w+dag", raw_source)
    if date:
        year = int(date.group(3))
        month = month_by_name.get(date.group(2).lower())
        day = int(date.group(1))
        return datetime.datetime(year, month, day)

def get_date_str(raw_source):
    date = re.search(r"(\d\d? \w+ \d{4} \w+dag)", raw_source)
    if date:
        return date.group(1)
