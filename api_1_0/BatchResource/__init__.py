#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

batch_blueprint = Blueprint('Batch', __name__)

from . import urls
