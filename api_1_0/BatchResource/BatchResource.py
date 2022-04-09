#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.BatchController import BatchController
from utils import commons
from utils.response_code import RET


class BatchResource(Resource):

    # get
    @classmethod
    def get(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='args', required=False, help='BatchID参数类型不正确或缺失')
        parser.add_argument('Year', location='args', required=False, help='Year参数类型不正确或缺失')
        parser.add_argument('Term', location='args', required=False, help='Term参数类型不正确或缺失')
        parser.add_argument('Week', location='args', required=False, help='Week参数类型不正确或缺失')
        parser.add_argument('IsCurrent', location='args', required=False, help='IsCurrent参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = BatchController.get(**kwargs)

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
            parser.add_argument('BatchID', location='form', required=False, help='BatchID参数类型不正确或缺失')
            parser.add_argument('Year', location='form', required=False, help='Year参数类型不正确或缺失')
            parser.add_argument('Term', location='form', required=False, help='Term参数类型不正确或缺失')
            parser.add_argument('Week', location='form', required=False, help='Week参数类型不正确或缺失')
            parser.add_argument('IsCurrent', location='form', required=False, help='IsCurrent参数类型不正确或缺失')
            
            # Pass in the ID list for multiple deletions
            parser.add_argument('AutoID', type=str, location='form', required=False, help='AutoID参数类型不正确或缺失')

            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

        res = BatchController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='form', required=True, help='BatchID参数类型不正确或缺失')
        # parser.add_argument('Year', location='form', required=False, help='Year参数类型不正确或缺失')
        # parser.add_argument('Term', location='form', required=False, help='Term参数类型不正确或缺失')
        # parser.add_argument('Week', location='form', required=False, help='Week参数类型不正确或缺失')
        parser.add_argument('IsCurrent', location='form', required=False, help='IsCurrent参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        res = BatchController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        BatchList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('BatchList', type=str, location='form', required=False, help='BatchList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('BatchList'):
            res = BatchController.add_list(**kwargs)

        else:
            parser.add_argument('Year', location='form', required=True, help='Year参数类型不正确或缺失')
            parser.add_argument('Term', location='form', required=True, help='Term参数类型不正确或缺失')
            parser.add_argument('Week', location='form', required=True, help='Week参数类型不正确或缺失')
            parser.add_argument('IsCurrent', location='form', required=True, help='IsCurrent参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = BatchController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
