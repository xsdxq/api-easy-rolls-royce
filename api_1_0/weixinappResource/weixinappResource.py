#!/usr/bin/env python
# -*- coding:utf-8 -*-

from werkzeug.datastructures import FileStorage
from flask import jsonify
from flask_restful import Resource, reqparse
from utils import commons

from service.weinappService import WeixinappService
from utils.loggings import loggings
from utils.response_code import RET


class WeixinappResource(Resource):
    # 小程序端信息采集+图片上传
    @classmethod
    def infomation_collection(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='form', required=True, help='InfoSet参数类型不正确或缺失')
        parser.add_argument('StudentID', location='form', required=True, help='InfoSet参数类型不正确或缺失')
        parser.add_argument('Name', location='form', required=True, help='InfoSet参数类型不正确或缺失')
        parser.add_argument('Class', location='form', required=True, help='InfoSet参数类型不正确或缺失')
        parser.add_argument('FileName', location='form', required=True, help='InfoSet参数类型不正确或缺失')
        parser.add_argument('ImageUrl', location='form', required=True, help='InfoSet参数类型不正确或缺失')


        try:
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
        except Exception as e:
            loggings.exception(1, e)
            return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')

        res = WeixinappService.infomation_collection(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    @classmethod
    def Pic_upload(cls):
        parser = reqparse.RequestParser()
        parser.add_argument("Image", type=FileStorage, location="files", required=True, help="Image参数类型不正确或缺失")

        try:
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
        except Exception as e:
            loggings.exception(1, e)
            return jsonify(code=RET.PARAMERR, message='参数类型不正确或缺失', error='参数类型不正确或缺失')

        res = WeixinappService.Pic_upload(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
