# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Extract information from documents"""
from collections import Counter
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
    "january": 1,
    "february": 2,
    "march": 3,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "october": 10,
}

def get_body(raw_source):
    try:
        body_start = """**Body**"""
        body_start_index = raw_source.index(body_start) + len(body_start)
    except ValueError:
        body_start_index = 0

    try:
        body_end = """**Load-Date:**"""
        body_end_index = raw_source.index(body_end)
    except ValueError:
        body_end_index = len(raw_source)
    return raw_source[body_start_index:body_end_index].strip()


def get_title(raw_source):
    title = re.search(r"# \[\*{3}<u>(.+)</u>\*{3}\]", raw_source)
    if title:
        return re.sub(r"</u>.+?<u>", " ", title.group(1))


def get_length(raw_source):
    length = re.search(r"\*\*Length:\*\*\s(\d+)\swords", raw_source)
    if length:
        return int(length.group(1))


def get_date(raw_source):
    date = re.search(r"(?<!\*\*\s)\b(?P<day>\d\d?)\s(?P<month>[a-z]+?)\s(?P<year>\d{4})( \w+dag)?", raw_source, re.I)
    if date:
        year = int(date.group("year"))
        month = month_by_name.get(date.group("month").lower())
        day = int(date.group("day"))
        if month is None:
            print(date.group("month"), "matched as month")
            return
        return datetime.datetime(year, month, day)
    else:
        date = re.search(r"(?<!\*\*\s)\b(?P<month>[a-z]+?)\s(?P<day>\d\d?),\s(?P<year>\d{4})", raw_source, re.I)
        if date:
            year = int(date.group("year"))
            month = month_by_name.get(date.group("month").lower())
            day = int(date.group("day"))
            if month is None:
                print(date.group("month"), "matched as month")
                return
            return datetime.datetime(year, month, day)

def get_date_str(raw_source):
    date = re.search(r"\d\d? \w+ \d{4} \w+dag|(?<!\*\*\s)\b\w+ \d\d?, \d{4}", raw_source)
    if date:
        return date.group(0)

def get_byline(raw_source):
    byline = re.search(r"\*\*Byline:\*\*\s(.+)\n", raw_source)
    if byline:
        return byline.group(1)

def get_section(raw_source):
    section = re.search(r"\*\*Section:\*\*\s(.+)\n", raw_source)
    if section:
        return section.group(1)

def get_publication(raw_source):
    lines = raw_source.splitlines()
    if len(lines) > 4:
        return lines[4]

def get_search_terms_count(raw_source, case_sensitive=True) -> Counter:
    body_text = get_body(raw_source)
    terms = re.findall(r"\*{3}<u>([^<]+)</u>\*{3}", body_text) if body_text else []
    if not case_sensitive:
        terms = [t.lower() for t in terms]
    return Counter(terms)
