#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File:ImageIdentify.py
# Author:yuanronghao
# Time:2022/4/10 13:05
# Software:PyCharm

"""
    this is function description
"""
import re

from flask import jsonify
from paddleocr import PaddleOCR, draw_ocr

from utils.response_code import RET, error_map_EN


def GetMiddleStr(content, startStr, endStr):
    startIndex = content.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]


def ImageIdentify(img_path):
    # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

    # 正则匹配
    pattern_time1 = "检测时间.{,2}(\d{4}-\d{2}-\d{2})"
    pattern_time2 = ".{,2}(\d{4}-\d{2}-\d{2})核酸检测时间"
    pattern_name = "姓名[^\u4e00-\u9fa5]*([\u4e00-\u9fa5]*\W*)身份证"
    pattern_result = ".*(阳性|阴性).*"
    try:
        result = ocr.ocr(img_path, cls=True)
        retxt = ''
        for line in result:
            print(line)
            text = line[1][0]
            retxt = retxt + text

        re_name = re.findall(pattern_name, retxt)
        print("re_name", re_name)
        if len(re_name) > 0:
            name = re_name[0]
        else:
            re_name = GetMiddleStr(retxt, '姓名', '身份证')
            if len(re_name) > 0:
                name = re_name
            else:
                name = ""

        re_time = re.findall(pattern_time1, retxt)
        print("re_time", re_time)
        if len(re_time) > 0:
            time = re_time[0]
        # 更改匹配模式
        else:
            re_time = re.findall(pattern_time2, retxt)
            if len(re_time) > 0:
                time = re_time[0]
            else:
                time = ""

        re_check_result = re.findall(pattern_result, retxt)
        print("check_result", re_check_result)
        if len(re_check_result) > 0:
            check_result = re_check_result[0]
            if check_result not in ['阴性', '阳性']:
                check_result = '无法识别'

        else:
            check_result = "无法识别"

        # if name and time and check_result != None:

        # 识别结果
        re_data = {
            "name": name,
            "time": time,
            "result": check_result,
        }

        return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': re_data}

        # else:
        #     return {'code': RET.IMAGEERR, 'message': "图像识别失败，可能上传了非核酸检测结果截图", 'data': "图像识别失败，可能上传了非核酸检测结果截图"}

    except Exception as e:
        return {'code': RET.IMAGEERR, 'message': "图像识别失败，请上传北京健康宝/支付宝健康码截图", 'data': "图像识别失败，请上传北京健康宝/支付宝健康码截图"}
