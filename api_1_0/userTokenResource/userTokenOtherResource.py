#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify
from service.userTokenService import UserTokenService
from utils import commons
from utils.loggings import loggings
from utils.response_code import RET


class UserTokenOtherResource(Resource):

    # join table query
    @classmethod
    def joint_query(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('UserType', type=int, location='args', required=False, help='UserType参数类型不正确或缺失')
        parser.add_argument('Token', type=str, location='args', required=False, help='Token参数类型不正确或缺失')
        parser.add_argument('ExpireTime', type=str, location='args', required=False, help='ExpireTime参数类型不正确或缺失')
        parser.add_argument('LoginIP', type=str, location='args', required=False, help='LoginIP参数类型不正确或缺失')
        parser.add_argument('LastLoginTime', type=str, location='args', required=False, help='LastLoginTime参数类型不正确或缺失')
        parser.add_argument('IsValid', type=int, location='args', required=False, help='IsValid参数类型不正确或缺失')
        parser.add_argument('AddTime', type=str, location='args', required=False, help='AddTime参数类型不正确或缺失')
        
        parser.add_argument('Page', type=int, location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', type=int, location='args', required=False, help='Page参数类型不正确或缺失')
        
        try:
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
        except Exception as e:
            loggings.exception(1, e)
            return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')
        
        res = UserTokenService.joint_query(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalCount=res['totalCount'], totalPage=res['totalPage'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])
