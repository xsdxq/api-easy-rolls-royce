#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import hashlib
import os
import random
import string
import time

from flask import current_app, json

from utils import commons
from app import photos
from utils.loggings import loggings
from utils.response_code import RET, error_map_EN

# from PIL import Image

from controller.testInfoController import TestInfoController
from controller.BatchController import BatchController


class WeixinappService(TestInfoController):

    @classmethod
    def infomation_collection(cls, **kwargs):

        # 图像识别
        from utils.ImageIdentify import ImageIdentify
        local_image_url = os.path.join(current_app.config['PICTURE_DEAFULT_DEST_PREFIX'], kwargs.get('FileName'))
        Identify_result = ImageIdentify(local_image_url)
        # 识别成功
        if Identify_result['code'] == RET.OK:
            data = Identify_result['data']

            kwargs.pop('FileName')
            kwargs.update(**{
                'TestTime': data['time'],
                'TestResults': data['result'],
                'NameInImage': data['name'],
            })

            if kwargs.get('Name') != kwargs['NameInImage']:
                kwargs['NameTest'] = 1
            else:
                kwargs['NameTest'] = 0

            # 信息入库
            # 1.检查该批次是否存在该学生信息
            try:
                res_get_BatchID = BatchController.get(**{
                    'IsCurrent': 1
                })
                if res_get_BatchID['code'] == RET.OK:
                    batch_id = res_get_BatchID['data'][0]['BatchID']
                    print("batch_id:", batch_id)
                else:
                    batch_id = None

                get_res = TestInfoController.get(**{
                    "BatchID": batch_id,
                    "StudentID": kwargs['StudentID'],
                })

                kwargs.update(**{
                    "BatchID": batch_id
                })
                if get_res['code'] == RET.OK:
                    if get_res['totalCount'] > 0:
                        kwargs.update(**{
                            'RecordID': get_res['data'][0]['RecordID'],
                        })
                        print(kwargs)
                        update_res = TestInfoController.update(**kwargs)

                    if get_res['totalCount'] == 0:
                        print(kwargs)
                        add_res = TestInfoController.add(**kwargs)

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
            # image_url = photos.url(file_name)
            # image_url=image_url[:4]+"s"+image_url[4:]
            loacl_ip = current_app.config['LOCAL_IP']
            image_url = "http://" + loacl_ip + ':5200/' + '_uploads/photos/' + filename
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

        return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': kwargs}
