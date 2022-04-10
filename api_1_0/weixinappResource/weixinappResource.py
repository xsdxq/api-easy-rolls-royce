#!/usr/bin/env python
# -*- coding:utf-8 -*-

from werkzeug.datastructures import FileStorage
from flask import jsonify
from flask_restful import Resource, reqparse
from utils import commons

from service.weinappService import WeixinappService


class WeixinappResource(Resource):
    # 小程序端信息采集+图片上传
    @classmethod
    def infomation_collection(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('BatchID', location='form', required=True, help='BatchID参数类型不正确或缺失')
        parser.add_argument('StudentID', location='form', required=True, help='StudentID参数类型不正确或缺失')
        parser.add_argument('Class', location='form', required=True, help='Class参数类型不正确或缺失')
        parser.add_argument('Name', location='form', required=True, help='Name参数类型不正确或缺失')
        parser.add_argument("Image", type=FileStorage, location="files", required=True, nullable=False,
                            help="Image参数类型不正确或缺失")

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = WeixinappService.infomation_collection(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
