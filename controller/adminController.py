#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.adminModel import Admin
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class AdminController(Admin):

    # add
    @classmethod
    def add(cls, **kwargs):
        
        try:
            model = Admin(
                AdminID=kwargs.get('AdminID'),
                NickName=kwargs.get('NickName'),
                Account=kwargs.get('Account'),
                AdminPassword=kwargs.get('AdminPassword'),
                CreateTime=kwargs.get('CreateTime'),
                IsDelete=kwargs.get('IsDelete'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'AutoID': model.AutoID,
                
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
            filter_list = []
            if kwargs.get('AutoID'):
                filter_list.append(cls.AutoID == kwargs['AutoID'])
            else:
                if kwargs.get('AutoID') is not None:
                    filter_list.append(cls.AutoID == kwargs.get('AutoID'))
                if kwargs.get('AdminID'):
                    filter_list.append(cls.AdminID == kwargs.get('AdminID'))
                if kwargs.get('NickName'):
                    filter_list.append(cls.NickName == kwargs.get('NickName'))
                if kwargs.get('Account'):
                    filter_list.append(cls.Account == kwargs.get('Account'))
                if kwargs.get('AdminPassword'):
                    filter_list.append(cls.AdminPassword == kwargs.get('AdminPassword'))
                if kwargs.get('CreateTime'):
                    filter_list.append(cls.CreateTime == kwargs.get('CreateTime'))
                if kwargs.get('IsDelete') is not None:
                    filter_list.append(cls.IsDelete == kwargs.get('IsDelete'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            admin_info = db.session.query(cls).filter(*filter_list)
            
            count = admin_info.count()
            pages = math.ceil(count / size)
            admin_info = admin_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(admin_info)
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
            filter_list = []
            if kwargs.get('AutoID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('AutoID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.AutoID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('AutoID') is not None:
                    filter_list.append(cls.AutoID == kwargs.get('AutoID'))
                if kwargs.get('AdminID'):
                    filter_list.append(cls.AdminID == kwargs.get('AdminID'))
                if kwargs.get('NickName'):
                    filter_list.append(cls.NickName == kwargs.get('NickName'))
                if kwargs.get('Account'):
                    filter_list.append(cls.Account == kwargs.get('Account'))
                if kwargs.get('AdminPassword'):
                    filter_list.append(cls.AdminPassword == kwargs.get('AdminPassword'))
                if kwargs.get('CreateTime'):
                    filter_list.append(cls.CreateTime == kwargs.get('CreateTime'))
                if kwargs.get('IsDelete') is not None:
                    filter_list.append(cls.IsDelete == kwargs.get('IsDelete'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'AutoID': []
            }
            for query_model in res.all():
                results['AutoID'].append(query_model.AutoID)

            res.delete()
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
            
            filter_list = []
            filter_list.append(cls.AutoID == kwargs.get('AutoID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'AutoID': res.first().AutoID,
                
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
        param_list = json.loads(kwargs.get('AdminList'))
        model_list = []
        for param_dict in param_list:
            
            model = Admin(
                AdminID=param_dict.get('AdminID'),
                NickName=param_dict.get('NickName'),
                Account=param_dict.get('Account'),
                AdminPassword=param_dict.get('AdminPassword'),
                CreateTime=param_dict.get('CreateTime'),
                IsDelete=param_dict.get('IsDelete'),
                
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
