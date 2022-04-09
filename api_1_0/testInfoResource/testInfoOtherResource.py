#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import jsonify
from flask_restful import Resource, reqparse

from utils import commons, loggings
from utils.response_code import RET
from service.testInfoService import TestInfoService

class TestInfoOtherResource(Resource):

	# join table query
	@classmethod
	def joint_query(cls):
		parser = reqparse.RequestParser()
		parser.add_argument('BatchID', location='form', required=False, help='BatchID参数类型不正确或缺失')
		parser.add_argument('StudentID', location='form', required=False, help='StudentID参数类型不正确或缺失')
		parser.add_argument('Class', location='form', required=False, help='Class参数类型不正确或缺失')
		parser.add_argument('Name', location='form', required=False, help='Name参数类型不正确或缺失')

		parser.add_argument('IsDelete', type=int, location='args', required=False, help='IsDelete参数类型不正确或缺失')
		parser.add_argument('CreateTime', type=str, location='args', required=False, help='CreateTime参数类型不正确或缺失')

		parser.add_argument('Page', type=int, location='args', required=False, help='Page参数类型不正确或缺失')
		parser.add_argument('Size', type=int, location='args', required=False, help='Page参数类型不正确或缺失')

		try:
			kwargs = parser.parse_args()
			kwargs = commons.put_remove_none(**kwargs)
		except Exception as e:
			loggings.exception(1, e)
			return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')

		res = TestInfoService.joint_query(**kwargs)
		if res['code'] == RET.OK:
			return jsonify(code=res['code'], message=res['message'], data=res['data'], totalCount=res['totalCount'],
						   totalPage=res['totalPage'])
		else:
			return jsonify(code=res['code'], message=res['message'], error=res['error'])
	pass
