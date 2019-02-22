#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Bojan"
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Bojan"
__status__ = "Development"

from flask import Flask

app = Flask(__name__)
app.config.from_object('app.config')
from app import game, gui

