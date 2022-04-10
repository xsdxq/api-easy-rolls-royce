#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

weixinapp_blueprint = Blueprint('weixinapp', __name__)

from . import urls
