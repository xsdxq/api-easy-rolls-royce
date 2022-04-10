#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import hashlib
import os
import random
import string
import time

from flask import current_app

from app import photos
from utils.response_code import RET, error_map_EN

# from PIL import Image

from controller.testInfoController import TestInfoController


class WeixinappService(TestInfoController):

    @classmethod
    def infomation_collection(cls, **kwargs):
        filename = kwargs.get("Image").filename
        # 去掉文件后缀末尾双引号
        ext = filename.rsplit('.', 1)[1].replace("\"", "").replace("\"", "")

        # 对图片保存名称唯一
        time_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        filename = str(int(time.time())) + time_str

        # 上传图片
        try:
            file_name = photos.save(kwargs.get("Image"), folder=None, name=filename + '.' + ext)
        except Exception as e:
            current_app.logger.error(e)
            return {'code': RET.THIRDERR, 'message': "上传图片失败，只支持jpg,png类型", 'error': '上传图片失败，只支持jpg,png类型'}

        # 获得保存后的图片路径
        try:
            image_url = photos.url(file_name)
            base_name = photos.get_basename(file_name).rsplit('.', 1)[0]

            # c_url = create_thumbnail(base_name, ext)
        except Exception as e:
            current_app.logger.error(e)
            return {'code': RET.THIRDERR, 'message': "获取图片路径失败！", 'error': "获取图片路径失败"}

        # 图像识别
        from utils.ImageIdentify import ImageIdentify
        local_image_url = os.path.join(current_app.config['PICTURE_DEAFULT_DEST_PREFIX'], filename + '.' + ext)
        Identify_result = ImageIdentify(local_image_url)
        # 识别成功
        if Identify_result['code'] == RET.OK:
            data = Identify_result['data']
            print(data)
            print(kwargs)
            kwargs.pop('Image')
            kwargs.update(**{
                'TestTime': data['time'],
                'TestResults': data['result'],
                'NameInImage': data['name'],
                'ImageUrl': image_url,
            })

            # 识别信息、图片url入库
            add_res = TestInfoController.add(**kwargs)
            if add_res['code'] != RET.OK:
                return add_res

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': data}






        # 失败
        else:
            return Identify_result
