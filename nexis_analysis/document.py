# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Extract information from documents"""
import datetime
import pathlib
import re

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

class NexisDocument:

    def __init__(self, file_name):
        """Create a NexisDocument by loading a GFM file"""
        with open(file_name, "r", encoding="utf-8") as fh:
            self.raw_source = fh.read()

    @property
    def body(self):

        body_start = """**Body**"""
        body_start_index = self.raw_source.index(body_start) + len(body_start)
        body_end = """**Load-Date:**"""
        body_end_index = self.raw_source.index(body_end)
        return self.raw_source[body_start_index:body_end_index].strip()

    @property
    def title(self):
        title = re.search(r"# \[\*{3}<u>(.+)</u>\*{3}\]", self.raw_source)
        if title:
            return title.group(1).replace("</u>*** ***<u>", " ")

    @property
    def length(self):
        length = re.search(r"\*\*Length:\*\*\s(\d+)\swords", self.raw_source)
        if length:
            return int(length.group(1))

    @property
    def date(self):
        date = re.search(r"(\d\d?) (\w+) (\d{4}) \w+dag", self.raw_source)
        if date:
            year = int(date.group(3))
            month = month_by_name.get(date.group(2).lower())
            day = int(date.group(1))
            return datetime.datetime(year, month, day)

    @property
    def date_str(self):
        date = re.search(r"(\d\d? \w+ \d{4} \w+dag)", self.raw_source)
        if date:
            return date.group(1)
