# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Representation of Nexis Uni documents"""
import datetime

class NexisDocument(object):
    body: str
    title: str
    length: int
    date_str: str
    date: datetime.datetime
    raw_source: str

    def __init__(self, raw_source: str):
        """Create a NexisDocument from GFM text"""
        self.raw_source = raw_source
        self.body = None
        self.title = None
        self.length = None
        self.date_str = None
        self.date = None
