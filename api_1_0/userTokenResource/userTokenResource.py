#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify
from controller.userTokenController import UserTokenController
from utils import commons
from utils.response_code import RET


class UserTokenResource(Resource):

    # get
    def get(self, UserID=None):
        if UserID:
            kwargs = {
                'UserID': UserID
            }
        
            res = UserTokenController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], error=res['error'])
                
        parser = reqparse.RequestParser()
        parser.add_argument('UserType', type=int, location='args', required=False, help='UserType参数类型不正确或缺失')
        parser.add_argument('Token', type=str, location='args', required=False, help='Token参数类型不正确或缺失')
        parser.add_argument('ExpireTime', type=str, location='args', required=False, help='ExpireTime参数类型不正确或缺失')
        parser.add_argument('LoginIP', type=str, location='args', required=False, help='LoginIP参数类型不正确或缺失')
        parser.add_argument('LastLoginTime', type=str, location='args', required=False, help='LastLoginTime参数类型不正确或缺失')
        parser.add_argument('IsValid', type=int, location='args', required=False, help='IsValid参数类型不正确或缺失')
        parser.add_argument('AddTime', type=str, location='args', required=False, help='AddTime参数类型不正确或缺失')
        
        parser.add_argument('Page', type=int, location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', type=int, location='args', required=False, help='Size参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        
        res = UserTokenController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error']) 
            
    # delete
    def delete(self, UserID=None):
        if UserID:
            kwargs = {
                'UserID': UserID
            }
        
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('UserType', type=int, location='form', required=False, help='UserType参数类型不正确或缺失')
            parser.add_argument('Token', type=str, location='form', required=False, help='Token参数类型不正确或缺失')
            parser.add_argument('ExpireTime', type=str, location='form', required=False, help='ExpireTime参数类型不正确或缺失')
            parser.add_argument('LoginIP', type=str, location='form', required=False, help='LoginIP参数类型不正确或缺失')
            parser.add_argument('LastLoginTime', type=str, location='form', required=False, help='LastLoginTime参数类型不正确或缺失')
            parser.add_argument('IsValid', type=int, location='form', required=False, help='IsValid参数类型不正确或缺失')
            parser.add_argument('AddTime', type=str, location='form', required=False, help='AddTime参数类型不正确或缺失')
            
            parser.add_argument('UserID', type=str, location='form', required=False, help='UserID参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
            
        res = UserTokenController.delete(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])

    # put
    def put(self, UserID):
        if not UserID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')
            
        parser = reqparse.RequestParser()
        parser.add_argument('UserType', type=int, location='form', required=False, help='UserType参数类型不正确或缺失')
        parser.add_argument('Token', type=str, location='form', required=False, help='Token参数类型不正确或缺失')
        parser.add_argument('ExpireTime', type=str, location='form', required=False, help='ExpireTime参数类型不正确或缺失')
        parser.add_argument('LoginIP', type=str, location='form', required=False, help='LoginIP参数类型不正确或缺失')
        parser.add_argument('LastLoginTime', type=str, location='form', required=False, help='LastLoginTime参数类型不正确或缺失')
        parser.add_argument('IsValid', type=int, location='form', required=False, help='IsValid参数类型不正确或缺失')
        parser.add_argument('AddTime', type=str, location='form', required=False, help='AddTime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['UserID'] = UserID
            
        res = UserTokenController.update(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])

    # add
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('UserTokenList', type=str, location='form', required=False, help='UserTokenList参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        
        if kwargs.get('UserTokenList'):
            res = UserTokenController.add_list(**kwargs)
              
        else:
            parser.add_argument('UserType', type=int, location='form', required=True, help='UserType参数类型不正确或缺失')
            parser.add_argument('Token', type=str, location='form', required=True, help='Token参数类型不正确或缺失')
            parser.add_argument('ExpireTime', type=str, location='form', required=True, help='ExpireTime参数类型不正确或缺失')
            parser.add_argument('LoginIP', type=str, location='form', required=True, help='LoginIP参数类型不正确或缺失')
            parser.add_argument('LastLoginTime', type=str, location='form', required=True, help='LastLoginTime参数类型不正确或缺失')
            parser.add_argument('IsValid', type=int, location='form', required=True, help='IsValid参数类型不正确或缺失')
            parser.add_argument('AddTime', type=str, location='form', required=True, help='AddTime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
            
            res = UserTokenController.add(**kwargs)
            
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])
