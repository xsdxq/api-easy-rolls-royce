#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import jsonify
from flask_restful import Resource, reqparse

from utils import commons, loggings
from utils.response_code import RET
from service.BatchService import BatchService


class BatchOtherResource(Resource):
	# get_IsCurrent
	@classmethod
	def batch_query(cls):
		parser = reqparse.RequestParser()

		parser.add_argument('IsDelete', type=int, location='args', required=False, help='IsDelete参数类型不正确或缺失')
		parser.add_argument('CreateTime', type=str, location='args', required=False, help='CreateTime参数类型不正确或缺失')


		try:
			kwargs = parser.parse_args()
			kwargs = commons.put_remove_none(**kwargs)
		except Exception as e:
			loggings.exception(1, e)
			return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')

		res = BatchService.get_isCurrent(**kwargs)
		if res['code'] == RET.OK:
			return jsonify(code=res['code'], message=res['message'], data=res['data'])
		else:
			return jsonify(code=res['code'], message=res['message'], error=res['error'])
