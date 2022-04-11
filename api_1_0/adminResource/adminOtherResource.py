#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify
from service.adminService import AdminService
from utils import commons
from utils.loggings import loggings
from utils.response_code import RET


class AdminOtherResource(Resource):
	# 普通管理员登录
	@classmethod
	def admin_login(cls):
		parser = reqparse.RequestParser()
		parser.add_argument('AccountNumber', type=str, location='form', required=False, help='AccountNumber参数类型不正确或缺失')
		parser.add_argument('AdminPassword', type=str, location='form', required=False, help='AdminPassword参数类型不正确或缺失')
		parser.add_argument('VerifyCodeID', type=str, location='form', required=False, help='VerifyCodeID参数类型不正确或缺失')
		parser.add_argument('VerifyCode', type=str, location='form', required=False, help='VerifyCode参数类型不正确或缺失')

		kwargs = parser.parse_args()
		kwargs = commons.put_remove_none(**kwargs)
		result = AdminService.admin_login(**kwargs)

		if result['code'] != '2000':
			return jsonify(code=result['code'], message=result['message'], error=result['error'])
		return jsonify(code=RET.OK, message=result['message'], data=result['data'])
