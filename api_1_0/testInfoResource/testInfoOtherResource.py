#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import jsonify
from flask_restful import Resource, reqparse
from utils.loggings import loggings
from utils import commons
from utils.response_code import RET
from service.testInfoService import TestInfoService
from controller.testInfoController import TestInfoController
from service.BatchService import BatchService
from flask import send_from_directory
from flask import make_response


class TestInfoOtherResource(Resource):
    # 生成excel
    @classmethod
    def get_excel(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='args', required=False, help='BatchID参数类型不正确或缺失')
        parser.add_argument('Grade', location='args', required=False, help='Grade类型不正确或缺失')

        try:
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
        except Exception as e:
            loggings.exception(1, e)
            return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')

        res = TestInfoService.get_excel(**kwargs)

        try:
            if res['code'] == RET.OK:
                file_path = res['file_path']
                filename = res['file_name']
                # response = make_response(send_from_directory(file_path, filename, as_attachment=True))
                # response.headers["Content-Disposition"] = "attachment; filename={}".format(
                #     filename.encode().decode('latin-1'))
                # return response
                return send_from_directory(file_path, filename, as_attachment=True)
            else:
                return jsonify(code=res['code'], message=res['message'], error=res['error'])

        except Exception as e:
            loggings.exception(1, e)
            return jsonify(code=RET.IOERR, message="文件下载异常:下载文件不存在")

    # join table query
    @classmethod
    def joint_query(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='args', required=False, help='BatchID参数类型不正确或缺失')
        parser.add_argument('StudentID', location='args', required=False, help='StudentID参数类型不正确或缺失')
        parser.add_argument('Grade', location='args', required=False, help='Class参数类型不正确或缺失')
        parser.add_argument('Class', location='args', required=False, help='Class参数类型不正确或缺失')
        parser.add_argument('Name', location='args', required=False, help='Name参数类型不正确或缺失')

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


    #unsubmit
    @classmethod
    def unsubmit_(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='args', required=False, help='BatchID参数类型不正确或缺失')
        parser.add_argument('StudentID', location='args', required=False, help='StudentID参数类型不正确或缺失')
        parser.add_argument('Grade', location='args', required=False, help='Class参数类型不正确或缺失')
        parser.add_argument('Class', location='args', required=False, help='Class参数类型不正确或缺失')
        parser.add_argument('Name', location='args', required=False, help='Name参数类型不正确或缺失')

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

    @classmethod
    def test_delete(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('RecordID', location='form', required=True, help='BatchID参数类型不正确或缺失')

        try:
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
        except Exception as e:
            loggings.exception(1, e)
            return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')

        res = TestInfoService.test_delete(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])

    # 管理员修改异常记录
    @classmethod
    def info_update(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('RecordID', location='form', required=True, help='BatchID参数类型不正确或缺失')

        try:
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

        except Exception as e:
            loggings.exception(1, e)
            return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')

        res = TestInfoService.info_update(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])

    # 管理员修改检测结果异常记录
    @classmethod
    def result_update(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('RecordID', location='form', required=True, help='BatchID参数类型不正确或缺失')

        try:
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
        except Exception as e:
            loggings.info(1, e)
            return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')

        kwargs.update(**{'TestResults': '阴性'})
        res = TestInfoController.update(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])

    @classmethod
    def unsubmit_query(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='args', required=True, help='BatchID参数类型不正确或缺失')
        parser.add_argument('Grade', location='args', required=False, help='Class参数类型不正确或缺失')
        parser.add_argument('Class', location='args', required=False, help='Class参数类型不正确或缺失')

        parser.add_argument('Page', type=int, location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', type=int, location='args', required=False, help='Page参数类型不正确或缺失')

        try:
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
        except Exception as e:
            loggings.exception(1, e)
            return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')

        res = TestInfoService.unsubmit_query(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalCount=res['totalCount'],
                           totalPage=res['totalPage'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])