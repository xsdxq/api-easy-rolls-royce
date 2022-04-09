#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.testInfoController import TestInfoController
from utils import commons
from utils.response_code import RET


class TestInfoResource(Resource):

    # get
    @classmethod
    def get(cls, RecordID=None):
        if RecordID:
            kwargs = {
                'RecordID': RecordID
            }

            res = TestInfoController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='args', required=False, help='BatchID参数类型不正确或缺失')
        parser.add_argument('StudentID', location='args', required=False, help='StudentID参数类型不正确或缺失')
        parser.add_argument('Class', location='args', required=False, help='Class参数类型不正确或缺失')
        parser.add_argument('Name', location='args', required=False, help='Name参数类型不正确或缺失')
        parser.add_argument('TestTime', location='args', required=False, help='TestTime参数类型不正确或缺失')
        parser.add_argument('ImageUrl', location='args', required=False, help='ImageUrl参数类型不正确或缺失')
        parser.add_argument('TestResults', location='args', required=False, help='TestResults参数类型不正确或缺失')
        parser.add_argument('CreateTime', location='args', required=False, help='CreateTime参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = TestInfoController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, RecordID=None):
        if RecordID:
            kwargs = {
                'RecordID': RecordID
            }

        else:
            parser = reqparse.RequestParser()
            parser.add_argument('BatchID', location='form', required=False, help='BatchID参数类型不正确或缺失')
            parser.add_argument('StudentID', location='form', required=False, help='StudentID参数类型不正确或缺失')
            parser.add_argument('Class', location='form', required=False, help='Class参数类型不正确或缺失')
            parser.add_argument('Name', location='form', required=False, help='Name参数类型不正确或缺失')
            parser.add_argument('TestTime', location='form', required=False, help='TestTime参数类型不正确或缺失')
            parser.add_argument('ImageUrl', location='form', required=False, help='ImageUrl参数类型不正确或缺失')
            parser.add_argument('TestResults', location='form', required=False, help='TestResults参数类型不正确或缺失')
            parser.add_argument('CreateTime', location='form', required=False, help='CreateTime参数类型不正确或缺失')
            
            # Pass in the ID list for multiple deletions
            parser.add_argument('RecordID', type=str, location='form', required=False, help='RecordID参数类型不正确或缺失')

            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

        res = TestInfoController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, RecordID):
        if not RecordID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='form', required=False, help='BatchID参数类型不正确或缺失')
        parser.add_argument('StudentID', location='form', required=False, help='StudentID参数类型不正确或缺失')
        parser.add_argument('Class', location='form', required=False, help='Class参数类型不正确或缺失')
        parser.add_argument('Name', location='form', required=False, help='Name参数类型不正确或缺失')
        parser.add_argument('TestTime', location='form', required=False, help='TestTime参数类型不正确或缺失')
        parser.add_argument('ImageUrl', location='form', required=False, help='ImageUrl参数类型不正确或缺失')
        parser.add_argument('TestResults', location='form', required=False, help='TestResults参数类型不正确或缺失')
        parser.add_argument('CreateTime', location='form', required=False, help='CreateTime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['RecordID'] = RecordID

        res = TestInfoController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        TestInfoList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('TestInfoList', type=str, location='form', required=False, help='TestInfoList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('TestInfoList'):
            res = TestInfoController.add_list(**kwargs)

        else:
            parser.add_argument('BatchID', location='form', required=False, help='BatchID参数类型不正确或缺失')
            parser.add_argument('StudentID', location='form', required=False, help='StudentID参数类型不正确或缺失')
            parser.add_argument('Class', location='form', required=False, help='Class参数类型不正确或缺失')
            parser.add_argument('Name', location='form', required=False, help='Name参数类型不正确或缺失')
            parser.add_argument('TestTime', location='form', required=False, help='TestTime参数类型不正确或缺失')
            parser.add_argument('ImageUrl', location='form', required=False, help='ImageUrl参数类型不正确或缺失')
            parser.add_argument('TestResults', location='form', required=False, help='TestResults参数类型不正确或缺失')
            parser.add_argument('CreateTime', location='form', required=False, help='CreateTime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = TestInfoController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
