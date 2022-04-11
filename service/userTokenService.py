#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math

from app import db
from controller.userTokenController import UserTokenController
from models.userTokenModel import UserToken
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class UserTokenService(UserTokenController):
    @classmethod
    def joint_query(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('UserID'):
                filter_list.append(cls.UserID == kwargs.get('UserID'))
            if kwargs.get('UserType'):
                filter_list.append(cls.UserType == kwargs.get('UserType'))
            if kwargs.get('Token'):
                filter_list.append(cls.Token == kwargs.get('Token'))
            if kwargs.get('ExpireTime'):
                filter_list.append(cls.ExpireTime == kwargs.get('ExpireTime'))
            if kwargs.get('LoginIP'):
                filter_list.append(cls.LoginIP == kwargs.get('LoginIP'))
            if kwargs.get('LastLoginTime'):
                filter_list.append(cls.LastLoginTime == kwargs.get('LastLoginTime'))
            if kwargs.get('IsValid'):
                filter_list.append(cls.IsValid == kwargs.get('IsValid'))
            if kwargs.get('AddTime'):
                filter_list.append(cls.AddTime == kwargs.get('AddTime'))
          
            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            userToken_info = db.session.query(UserToken.UserID, UserToken.UserType, UserToken.Token, UserToken.ExpireTime, UserToken.LoginIP, UserToken.LastLoginTime, UserToken.IsValid, UserToken.AddTime).filter(*filter_list)
            
            count = userToken_info.count()
            pages = math.ceil(count / size)
            userToken_info = userToken_info.limit(size).offset((page - 1) * size).all()
            
            if not userToken_info:
                return {'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}
    
            # 处理返回的数据
            results = commons.query_to_dict(userToken_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}
        
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()
