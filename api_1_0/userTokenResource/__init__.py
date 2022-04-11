#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

usertoken_blueprint = Blueprint('userToken', __name__)

from . import urls
