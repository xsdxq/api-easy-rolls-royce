#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.adminController import AdminController
from utils import commons
from utils.response_code import RET


class AdminResource(Resource):

    # get
    @classmethod
    def get(cls, AutoID=None):
        if AutoID:
            kwargs = {
                'AutoID': AutoID
            }

            res = AdminController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('AdminID', location='args', required=False, help='AdminID参数类型不正确或缺失')
        parser.add_argument('NickName', location='args', required=False, help='NickName参数类型不正确或缺失')
        parser.add_argument('Account', location='args', required=False, help='Account参数类型不正确或缺失')
        parser.add_argument('AdminPassword', location='args', required=False, help='AdminPassword参数类型不正确或缺失')
        parser.add_argument('CreateTime', location='args', required=False, help='CreateTime参数类型不正确或缺失')
        parser.add_argument('IsDelete', location='args', required=False, help='IsDelete参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = AdminController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, AutoID=None):
        if AutoID:
            kwargs = {
                'AutoID': AutoID
            }

        else:
            parser = reqparse.RequestParser()
            parser.add_argument('AdminID', location='form', required=False, help='AdminID参数类型不正确或缺失')
            parser.add_argument('NickName', location='form', required=False, help='NickName参数类型不正确或缺失')
            parser.add_argument('Account', location='form', required=False, help='Account参数类型不正确或缺失')
            parser.add_argument('AdminPassword', location='form', required=False, help='AdminPassword参数类型不正确或缺失')
            parser.add_argument('CreateTime', location='form', required=False, help='CreateTime参数类型不正确或缺失')
            parser.add_argument('IsDelete', location='form', required=False, help='IsDelete参数类型不正确或缺失')
            
            # Pass in the ID list for multiple deletions
            parser.add_argument('AutoID', type=str, location='form', required=False, help='AutoID参数类型不正确或缺失')

            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

        res = AdminController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, AutoID):
        if not AutoID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('AdminID', location='form', required=False, help='AdminID参数类型不正确或缺失')
        parser.add_argument('NickName', location='form', required=False, help='NickName参数类型不正确或缺失')
        parser.add_argument('Account', location='form', required=False, help='Account参数类型不正确或缺失')
        parser.add_argument('AdminPassword', location='form', required=False, help='AdminPassword参数类型不正确或缺失')
        parser.add_argument('CreateTime', location='form', required=False, help='CreateTime参数类型不正确或缺失')
        parser.add_argument('IsDelete', location='form', required=False, help='IsDelete参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['AutoID'] = AutoID

        res = AdminController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        AdminList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('AdminList', type=str, location='form', required=False, help='AdminList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('AdminList'):
            res = AdminController.add_list(**kwargs)

        else:
            parser.add_argument('AdminID', location='form', required=False, help='AdminID参数类型不正确或缺失')
            parser.add_argument('NickName', location='form', required=False, help='NickName参数类型不正确或缺失')
            parser.add_argument('Account', location='form', required=False, help='Account参数类型不正确或缺失')
            parser.add_argument('AdminPassword', location='form', required=False, help='AdminPassword参数类型不正确或缺失')
            parser.add_argument('CreateTime', location='form', required=False, help='CreateTime参数类型不正确或缺失')
            parser.add_argument('IsDelete', location='form', required=False, help='IsDelete参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = AdminController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
