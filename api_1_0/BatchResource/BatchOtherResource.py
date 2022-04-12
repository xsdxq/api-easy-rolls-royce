#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import jsonify
from flask_restful import Resource, reqparse

from utils import commons, loggings
from utils.response_code import RET
from service.BatchService import BatchService


class BatchOtherResource(Resource):
	pass

