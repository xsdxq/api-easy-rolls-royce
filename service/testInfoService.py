#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
import datetime

from controller.testInfoController import TestInfoController
from models.testInfoModel import TestInfo
from utils import commons, loggings
from utils.response_code import RET, error_map_EN
from app import db


class TestInfoService(TestInfoController):

    @classmethod
    def test_delete(cls, **kwargs):
        filter_list = []
        filter_list.append(cls.IsDelete == 0)
        if kwargs.get('RecordID'):
            filter_list.append(cls.RecordID == kwargs.get('RecordID'))

        # page = int(kwargs.get('Page', 1))
        # size = int(kwargs.get('Size', 10))

        res = db.session.query(cls).filter(*filter_list).with_for_update()

        results = {
            'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'RecordID': []
        }

        for query_model in res.all():
            results['RecordID'].append(query_model.RecordID)

        res.update({'IsDelete': 1})
        db.session.commit()

        return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}





    # 列表查询
    @classmethod
    def joint_query(cls, **kwargs):
        try:
            filter_list = []
            filter_list.append(cls.IsDelete == 0)
            if kwargs.get('Class'):
                filter_list.append(cls.Class == kwargs.get('Class'))
            if kwargs.get('Name'):
                filter_list.append(cls.Name == kwargs.get('Name'))
            if kwargs.get('BatchID'):
                filter_list.append(cls.BatchID == kwargs.get('BatchID'))
            if kwargs.get('StudentID'):
                filter_list.append(cls.StudentID == kwargs.get('StudentID'))

            if kwargs.get('IsDelete'):
                filter_list.append(cls.IsDelete == kwargs.get('IsDelete'))
            if kwargs.get('CreateTime'):
                filter_list.append(cls.CreateTime == kwargs.get('CreateTime'))

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))

            task_info = db.session.query(
                TestInfo.RecordID,
                TestInfo.StudentID,
                TestInfo.BatchID,
                TestInfo.Name,
                TestInfo.Class,
                TestInfo.TestTime,
                TestInfo.TestResults,
                TestInfo.ImageUrl,
                TestInfo.CreateTime,
            ).filter(*filter_list)

            count = task_info.count()
            pages = math.ceil(count / size)
            task_info = task_info.limit(size).offset((page - 1) * size).all()

            if not task_info:
                return {'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}

            # 处理返回的数据
            results = commons.query_to_dict(task_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages,
                    'data': results}

        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

    @classmethod
    #小程序信息提交和图片上传识别
    def infosubmit(cls, **kwargs):




        pass






















