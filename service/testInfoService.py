#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
import datetime
import os

from xlwt import Workbook
from sqlalchemy import and_, case
from controller.testInfoController import TestInfoController
from service.BatchService import BatchService
from models.testInfoModel import TestInfo
from utils import commons, loggings
from utils.response_code import RET, error_map_EN
from app import db
from flask import current_app


class TestInfoService(TestInfoController):

    # 生成excel
    @classmethod
    def get_excel(cls, **kwargs):
        try:
            filter_list = [cls.IsDelete == 0]
            if kwargs.get('BatchID'):
                filter_list.append(cls.BatchID == kwargs.get('BatchID'))
            if kwargs.get('Grade'):
                filter_list.append(cls.Grade == kwargs.get('Grade'))

            task_info = db.session.query(
                TestInfo.Class,
                TestInfo.Name,
                TestInfo.StudentID,
                TestInfo.TestTime,
                TestInfo.TestResults,
            ).filter(*filter_list).all()

            # if not task_info:
            #     return {'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}

            # 处理返回的数据
            results = commons.query_to_dict(task_info)
            info_value = []
            for i, x in enumerate(results):
                info = list(x.values())
                index = [str(i + 1)]
                info_value.append(index + info)

            # import xlwt
            file = Workbook(encoding='utf-8')
            # 指定file以utf-8的格式打开
            table = file.add_sheet('data')
            header = ['序号', '班级', '姓名', '学号', '检测时间', '检测结果']
            for a in range(6):
                table.write(0, a, header[a])
            for i, p in enumerate(info_value):
                # 将数据写入文件,i是enumerate()函数返回的序号数
                for j, q in enumerate(p):
                    table.write(i + 1, j, q)
            file.save('data.xls')
            file_path = os.getcwd()
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'file_path': file_path, 'file_name': 'data.xls'}

        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

    # 删除信息记录
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

    # 查询信息记录
    @classmethod
    def joint_query(cls, **kwargs):
        try:
            filter_list = [cls.IsDelete == 0]
            # 模糊查询
            if kwargs.get('Class'):
                class_text = kwargs.get('Class')
                filter_list.append(cls.Class.like('%' + class_text + '%'))
            if kwargs.get('Grade'):
                grade_text = kwargs.get('Grade')
                filter_list.append(cls.Grade.like('%' + grade_text + '%'))
            if kwargs.get('Name'):
                name_text = kwargs.get('Name')
                filter_list.append(cls.Name.like('%' + name_text + '%'))
            if kwargs.get('BatchID'):
                BatchID = kwargs.get('BatchID')
                filter_list.append(cls.BatchID.like('%' + BatchID + '%'))
            if kwargs.get('StudentID'):
                studentID = kwargs.get('StudentID')
                filter_list.append(cls.StudentID.like('%' + studentID + '%'))

            if kwargs.get('CreateTime'):
                filter_list.append(cls.CreateTime == kwargs.get('CreateTime'))

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))

            from models.BatchModel import Batch
            task_info = db.session.query(
                TestInfo.RecordID,
                TestInfo.StudentID,
                TestInfo.BatchID,
                TestInfo.Name,
                TestInfo.NameInImage,
                TestInfo.Class,
                TestInfo.Grade,
                TestInfo.TestTime,
                TestInfo.TestResults,
                TestInfo.ImageUrl,
                TestInfo.CreateTime,
                TestInfo.NameTest,
                Batch.Year,
                Batch.Term,
                Batch.Week
            ).filter(*filter_list) \
                .join(Batch, and_(Batch.BatchID == cls.BatchID, Batch.IsDelete == 0)) \
                .order_by(
                *(
                    case(value=cls.TestResults, whens={
                        "阴性": 3,
                        "无法识别": 2,
                        "阳性": 1,
                    }),
                    TestInfo.NameTest.desc(),
                    TestInfo.CreateTime.desc(),
                )
            )

            count = task_info.count()
            pages = math.ceil(count / size)
            task_info = task_info.limit(size).offset((page - 1) * size).all()

            # if not task_info:
            #     return {'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}

            # 处理返回的数据
            results = commons.query_to_dict(task_info)
            for x in results:
                batch_info = BatchService.get_info(x['BatchID'])
                if batch_info['code'] == RET.OK:
                    x['batch_info'] = batch_info['info'][0]
                else:
                    x['batch_info'] = ''
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages,
                    'data': results}

        except Exception as e:
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

    # 更新姓名识别异常
    @classmethod
    def info_update(cls, **kwargs):
        filter_list = []
        filter_list.append(cls.IsDelete == 0)
        if kwargs.get('RecordID'):
            filter_list.append(cls.RecordID == kwargs.get('RecordID'))
        kwargs['NameTest'] = 0

        res = db.session.query(cls).filter(*filter_list).with_for_update()
        if res.first():

            results = {
                # 'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'RecordID': res.first().RecordID,

            }
            res.update(kwargs)
            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
        else:
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': 'RecordID不存在'}
