#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import hashlib
import os
import random
import string
import time

# from PIL import Image
from werkzeug.datastructures import FileStorage
from app import photos
from flask import jsonify, current_app
from flask_restful import Resource, reqparse
from utils import commons, loggings
from utils.response_code import RET



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

        filename = kwargs.get("Image").filename
        # 去掉文件后缀末尾双引号
        ext = filename.rsplit('.', 1)[1].replace("\"", "").replace("\"", "")

        # 对图片保存名称唯一
        time_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        filename = str(int(time.time())) + time_str

        try:
            file_name = photos.save(kwargs.get("Image"), folder=None, name=filename + '.' + ext)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.THIRDERR, message="上传图片失败，只支持jpg,png类型")

        # res = TestInfoController.add(**kwargs)
        res = {
            "code": 2000,
            "message": " ",
            "data": ""
        }

        return jsonify(code=res['code'], message=res['message'], data=res['data'])


