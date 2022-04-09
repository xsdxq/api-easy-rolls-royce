#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controller.BatchController import BatchController
from models.BatchModel import Batch
from app import db
from utils.response_code import RET, error_map_EN
from utils import commons, loggings

class BatchService(BatchController):
    @classmethod
    def get_info(cls,**kwargs):
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

            task_info = db.session.query(
                Batch.Year,
                Batch.Term,
                Batch.Week,
            ).filter(*filter_list)

            if not task_info:
                return {'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}

                # 处理返回的数据
            results = commons.query_to_dict(task_info)
            info = results[0]+"年"+"第"+results[1]+"学期第"+results[2]+"周"
            return {info}

        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()
