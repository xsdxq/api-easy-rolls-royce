#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.testInfoModel import TestInfo
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class TestInfoController(TestInfo):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        RecordID = GenerateID.create_random_id()
        
        try:
            model = TestInfo(
                RecordID=RecordID,
                BatchID=kwargs.get('BatchID'),
                StudentID=kwargs.get('StudentID'),
                Class=kwargs.get('Class'),
                Name=kwargs.get('Name'),
                TestTime=kwargs.get('TestTime'),
                ImageUrl=kwargs.get('ImageUrl'),
                TestResults=kwargs.get('TestResults'),
                CreateTime=kwargs.get('CreateTime'),
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'RecordID': model.RecordID,
                
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
            if kwargs.get('RecordID'):
                filter_list.append(cls.RecordID == kwargs['RecordID'])
            else:
                if kwargs.get('BatchID'):
                    filter_list.append(cls.BatchID == kwargs.get('BatchID'))
                if kwargs.get('StudentID'):
                    filter_list.append(cls.StudentID == kwargs.get('StudentID'))
                if kwargs.get('Class'):
                    filter_list.append(cls.Class == kwargs.get('Class'))
                if kwargs.get('Name'):
                    filter_list.append(cls.Name == kwargs.get('Name'))
                if kwargs.get('TestTime'):
                    filter_list.append(cls.TestTime == kwargs.get('TestTime'))
                if kwargs.get('ImageUrl'):
                    filter_list.append(cls.ImageUrl == kwargs.get('ImageUrl'))
                if kwargs.get('TestResults'):
                    filter_list.append(cls.TestResults == kwargs.get('TestResults'))
                if kwargs.get('CreateTime'):
                    filter_list.append(cls.CreateTime == kwargs.get('CreateTime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            test_info_info = db.session.query(cls).filter(*filter_list)
            
            count = test_info_info.count()
            pages = math.ceil(count / size)
            test_info_info = test_info_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(test_info_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}
            
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

            filter_list = []
            filter_list.append(cls.IsDelete == 0)
            if kwargs.get('RecordID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('RecordID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.RecordID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('BatchID'):
                    filter_list.append(cls.BatchID == kwargs.get('BatchID'))
                if kwargs.get('StudentID'):
                    filter_list.append(cls.StudentID == kwargs.get('StudentID'))
                if kwargs.get('Class'):
                    filter_list.append(cls.Class == kwargs.get('Class'))
                if kwargs.get('Name'):
                    filter_list.append(cls.Name == kwargs.get('Name'))
                if kwargs.get('TestTime'):
                    filter_list.append(cls.TestTime == kwargs.get('TestTime'))
                if kwargs.get('ImageUrl'):
                    filter_list.append(cls.ImageUrl == kwargs.get('ImageUrl'))
                if kwargs.get('TestResults'):
                    filter_list.append(cls.TestResults == kwargs.get('TestResults'))
                if kwargs.get('CreateTime'):
                    filter_list.append(cls.CreateTime == kwargs.get('CreateTime'))
                
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
            filter_list.append(cls.RecordID == kwargs.get('RecordID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'RecordID': res.first().RecordID,
                
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
        param_list = json.loads(kwargs.get('TestInfoList'))
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            RecordID = GenerateID.create_random_id()
            
            model = TestInfo(
                RecordID=RecordID,
                BatchID=param_dict.get('BatchID'),
                StudentID=param_dict.get('StudentID'),
                Class=param_dict.get('Class'),
                Name=param_dict.get('Name'),
                TestTime=param_dict.get('TestTime'),
                ImageUrl=param_dict.get('ImageUrl'),
                TestResults=param_dict.get('TestResults'),
                CreateTime=param_dict.get('CreateTime'),
                
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
                added_record['RecordID'] = model.RecordID
                
                results['added_records'].append(added_record)
            
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
