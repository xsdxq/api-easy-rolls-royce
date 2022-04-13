#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controller.BatchController import BatchController
from models.BatchModel import Batch
from app import db
from utils.response_code import RET, error_map_EN
from utils import commons, loggings


class BatchService(BatchController):
    @classmethod
    def get_info(cls, kwargs):
        try:
            filter_list = [cls.BatchID == kwargs, cls.IsDelete == 0]
            task_info = db.session.query(
                Batch.Year,
                Batch.Term,
                Batch.Week,
            ).filter(*filter_list).all()

            if not task_info:
                return {'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}

            # 处理返回的数据
            results = commons.query_to_dict(task_info)
            batch_info = []
            for x in results:
                batch_info.append(x['Year'] + "年" + "第" + x['Term'] + "学期第" + x['Week'] + "周")

            return {'code': RET.OK, 'info': batch_info}

        except Exception as e:
            # loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

