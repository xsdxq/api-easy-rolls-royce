#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import current_app, request

from app import db
import math
import json
from sqlalchemy import or_
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from models.userTokenModel import UserToken
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class UserTokenController(UserToken):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        UserID = GenerateID.create_random_id()

        try:
            model = UserToken(
                UserID=UserID,
                UserType=kwargs.get('UserType'),
                Token=kwargs.get('Token'),
                ExpireTime=kwargs.get('ExpireTime'),
                LoginIP=kwargs.get('LoginIP'),
                LastLoginTime=kwargs.get('LastLoginTime'),
                IsValid=kwargs.get('IsValid'),
                AddTime=kwargs.get('AddTime'),

            )
            db.session.add(model)
            db.session.commit()
            results = commons.query_to_dict(model)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('UserID'):
                filter_list.append(cls.UserID == kwargs.get('UserID'))
            else:
                if kwargs.get('UserType') is not None:
                    filter_list.append(cls.UserType == kwargs.get('UserType'))
                if kwargs.get('Token'):
                    filter_list.append(cls.Token == kwargs.get('Token'))
                if kwargs.get('ExpireTime'):
                    filter_list.append(cls.ExpireTime == kwargs.get('ExpireTime'))
                if kwargs.get('LoginIP'):
                    filter_list.append(cls.LoginIP == kwargs.get('LoginIP'))
                if kwargs.get('LastLoginTime'):
                    filter_list.append(cls.LastLoginTime == kwargs.get('LastLoginTime'))
                if kwargs.get('IsValid') is not None:
                    filter_list.append(cls.IsValid == kwargs.get('IsValid'))
                if kwargs.get('AddTime'):
                    filter_list.append(cls.AddTime == kwargs.get('AddTime'))

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))

            user_token_info = db.session.query(cls).filter(*filter_list)

            count = user_token_info.count()
            pages = math.ceil(count / size)
            user_token_info = user_token_info.limit(size).offset((page - 1) * size).all()

            # judge whether the data is None
            if not user_token_info:
                return {'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No query results'}

            results = commons.query_to_dict(user_token_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages,
                    'data': results}

        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('UserID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('UserID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.UserID == primary_key)
                filter_list.append(or_(*primary_key_list))

            else:
                if kwargs.get('UserType') is not None:
                    filter_list.append(cls.UserType == kwargs.get('UserType'))
                if kwargs.get('Token'):
                    filter_list.append(cls.Token == kwargs.get('Token'))
                if kwargs.get('ExpireTime'):
                    filter_list.append(cls.ExpireTime == kwargs.get('ExpireTime'))
                if kwargs.get('LoginIP'):
                    filter_list.append(cls.LoginIP == kwargs.get('LoginIP'))
                if kwargs.get('LastLoginTime'):
                    filter_list.append(cls.LastLoginTime == kwargs.get('LastLoginTime'))
                if kwargs.get('IsValid') is not None:
                    filter_list.append(cls.IsValid == kwargs.get('IsValid'))
                if kwargs.get('AddTime'):
                    filter_list.append(cls.AddTime == kwargs.get('AddTime'))

            res = db.session.query(cls).filter(*filter_list).with_for_update().delete()
            if res < 1:
                return {'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to delete'}

            db.session.commit()
            return {'code': RET.OK, 'message': error_map_EN[RET.OK]}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

    # update
    @classmethod
    def update(cls, **kwargs):
        try:

            res = db.session.query(cls).filter(
                cls.UserID == kwargs.get('UserID')
            ).with_for_update().update(kwargs)

            if res < 1:
                return {'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}
            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK]}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

    # batch add
    @classmethod
    def add_list(cls, **kwargs):
        param_list = json.loads(kwargs.get('UserTokenList'))
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            UserID = GenerateID.create_random_id()

            model = UserToken(
                UserID=UserID,
                UserType=param_dict.get('UserType'),
                Token=param_dict.get('Token'),
                ExpireTime=param_dict.get('ExpireTime'),
                LoginIP=param_dict.get('LoginIP'),
                LastLoginTime=param_dict.get('LastLoginTime'),
                IsValid=param_dict.get('IsValid'),
                AddTime=param_dict.get('AddTime'),

            )
            model_list.append(model)

        try:
            db.session.add_all(model_list)
            db.session.commit()
            results = []
            for model in model_list:
                results.append(commons.query_to_dict(model))

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

    # get token
    @classmethod
    def get_token(cls, **kwargs):
        token = db.session.query(cls).filter(cls.UserID == kwargs.get('UserID'),
                                             cls.IsValid == 1)
        if not token:
            return None
        else:
            return token

    @classmethod
    def create_token(cls, _userid, _usertype):
        """
        生成新的token
        :param user_type: 用户类型，1--平台用户；2--管理员；
        :param _userID:用户id
        :param _userType:
        :return: token
        """
        # 第一个参数是内部的私钥(配置信息)，第二个参数是有效期(秒)
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=current_app.config["TOKEN_EXPIRES"])
        # 接受用户id转换编码
        token = s.dumps({"id": _userid, "user_type": _usertype}).decode("ascii")
        return token

    @classmethod
    # token信息持久化(保存到MySQL数据库中或者Redis中)；
    def save_token(cls, **kwargs):

        user_token = UserToken(
            AdminID=kwargs.get('AdminID'),
            UserType=kwargs.get('UserType'),
            Token=kwargs.get('Token'),
            ExpireTime=kwargs.get('ExpireTime'),
            LoginIP=request.remote_addr
        )
        try:
            db.session.add(user_token)
            db.session.commit()

        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return None
        # finally:
        #     db.session.close()

        return user_token
