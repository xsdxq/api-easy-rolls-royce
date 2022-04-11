#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import hashlib
import os
import random
import string
import time

from flask import current_app, json

from app import photos
from utils.loggings import loggings
from utils.response_code import RET, error_map_EN

# from PIL import Image

from controller.testInfoController import TestInfoController


class WeixinappService(TestInfoController):

    @classmethod
    def infomation_collection(cls, **kwargs):

        # A=kwargs.get('InfoSet')
        # print(A,type(A))
        # B=json.loads(A)
        # print(B,type(B))
        # C=json.loads(B)
        # print(C,type(C))
        info_set = json.loads(kwargs.get('InfoSet'))
        info_set = json.loads(info_set)
        print(info_set, type(info_set))


        # 图像识别
        from utils.ImageIdentify import ImageIdentify
        local_image_url = os.path.join(current_app.config['PICTURE_DEAFULT_DEST_PREFIX'], info_set['FileName'])
        Identify_result = ImageIdentify(local_image_url)
        # 识别成功
        if Identify_result['code'] == RET.OK:
            data = Identify_result['data']
            print(data)
            info_set.update(**{
                'TestTime': data['time'],
                'TestResults': data['result'],
                'NameInImage': data['name'],
            })

            # 信息入库
            # 1.检查该批次是否存在该学生信息
            try:
                get_res = TestInfoController.get(**{
                    "BatchID": info_set['BatchID'],
                    "StudentID": info_set['StudentID'],
                })

                if get_res['code'] == RET.OK:
                    if get_res['totalCount'] > 0:
                        info_set.upudate(**{
                            'RecordID': get_res['data'][0]['RecordID'],
                        })
                        update_res = TestInfoController.update(**info_set)

                    if get_res['totalCount'] == 0:
                        add_res = TestInfoController.add(**info_set)

            except Exception as e:
                loggings.exception(1, e)
                return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': data}

        # 失败
        else:
            return Identify_result

    # 图片上传,只上传，信息不入库
    @classmethod
    def Pic_upload(cls, **kwargs):
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
            return {'code': RET.THIRDERR, 'message': "上传图片失败，只支持jpg,png类型", 'data': {'error': str(e)}}

        # 获得保存后的图片路径
        try:
            image_url = photos.url(file_name)
            base_name = photos.get_basename(file_name).rsplit('.', 1)[0]

            # c_url = create_thumbnail(base_name, ext)
        except Exception as e:
            current_app.logger.error(e)
            return {'code': RET.THIRDERR, 'message': "获取图片路径失败！", 'data': {'error': str(e)}}

        FileName = filename + '.' + ext
        kwargs.pop('Image')
        kwargs.update(**{
            "ImageUrl": image_url,
            "FileName": FileName,
        })
        print(kwargs)

        data = json.dumps(kwargs)

        return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': data}
