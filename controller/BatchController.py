#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.BatchModel import Batch
from utils import commons
from utils.generate_id import GenerateID
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class BatchController(Batch):

    #当前批次重置
    @classmethod
    def check_before_addorupdate(cls, **kwargs):
        if kwargs.get('IsCurrent') == '1':
            filter_list = [cls.IsDelete == 0]
            filter_list.append(cls.IsCurrent == 1)
            Batch_info = db.session.query(cls).filter(*filter_list).all()
            results = commons.query_to_dict(Batch_info)
            # BatchIDs=[]
            for item in results:
                BatchID = item["BatchID"]
                cls.update(**{
                    "BatchID": BatchID,
                    "IsCurrent": 0,
                })

    @classmethod
    def update_check(cls, **kwargs):
        cls.check_before_addorupdate(**kwargs)
        res = cls.update(**kwargs)
        return res

    # add
    @classmethod
    def add(cls, **kwargs):
        try:
            # 如果新添加批次设为当前批次
            cls.check_before_addorupdate(**kwargs)

            model = Batch(
                BatchID=GenerateID.create_random_id(),
                Year=kwargs.get('Year'),
                Term=kwargs.get('Term'),
                Week=kwargs.get('Week'),
                IsCurrent=kwargs.get('IsCurrent'),
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'BatchID': model.BatchID,
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = [cls.IsDelete == 0]

            if kwargs.get('BatchID') is not None:
                filter_list.append(cls.BatchID == kwargs.get('BatchID'))
            if kwargs.get('Year'):
                filter_list.append(cls.Year == kwargs.get('Year'))
            if kwargs.get('Term'):
                filter_list.append(cls.Term == kwargs.get('Term'))
            if kwargs.get('Week'):
                filter_list.append(cls.Week == kwargs.get('Week'))
            if kwargs.get('IsCurrent') is not None:
                filter_list.append(cls.IsCurrent == kwargs.get('IsCurrent'))

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))

            Batch_info = db.session.query(cls).filter(*filter_list)

            count = Batch_info.count()
            pages = math.ceil(count / size)
            Batch_info = Batch_info.limit(size).offset((page - 1) * size).all()

            results = commons.query_to_dict(Batch_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages,
                    'data': results}

        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = [cls.IsDelete == 0]
            if kwargs.get('AutoID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('AutoID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.AutoID == primary_key)
                filter_list.append(or_(*primary_key_list))

            else:
                if kwargs.get('BatchID') is not None:
                    filter_list.append(cls.BatchID == kwargs.get('BatchID'))
                if kwargs.get('Year'):
                    filter_list.append(cls.Year == kwargs.get('Year'))
                if kwargs.get('Term'):
                    filter_list.append(cls.Term == kwargs.get('Term'))
                if kwargs.get('Week'):
                    filter_list.append(cls.Week == kwargs.get('Week'))
                if kwargs.get('IsCurrent') is not None:
                    filter_list.append(cls.IsCurrent == kwargs.get('IsCurrent'))

            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'AutoID': []
            }
            for query_model in res.all():
                results['AutoID'].append(query_model.AutoID)

            res.update({'IsDelete': 1})
            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # update
    @classmethod
    def update(cls, **kwargs):
        try:

            filter_list = [cls.IsDelete == 0]
            filter_list.append(cls.BatchID == kwargs.get('BatchID'))

            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'BatchID': res.first().BatchID,
            }

            res.update(kwargs)
            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # batch add
    @classmethod
    def add_list(cls, **kwargs):
        param_list = json.loads(kwargs.get('BatchList'))
        model_list = []
        for param_dict in param_list:
            model = Batch(
                AutoID=param_dict.get('AutoID'),
                BatchID=param_dict.get('BatchID'),
                Year=param_dict.get('Year'),
                Term=param_dict.get('Term'),
                Week=param_dict.get('Week'),
                IsCurrent=param_dict.get('IsCurrent'),

            )
            model_list.append(model)

        try:
            db.session.add_all(model_list)
            db.session.commit()
            results = {
                'added_records': [],
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            for model in model_list:
                added_record = {}
                added_record['AutoID'] = model.AutoID

                results['added_records'].append(added_record)

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
