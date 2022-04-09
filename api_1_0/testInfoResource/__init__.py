#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

testinfo_blueprint = Blueprint('testInfo', __name__)

from . import urls
