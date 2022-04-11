#!/usr/bin/env python
# -*- coding:utf-8 -*-
from controller import adminController
from controller.adminController import AdminController
import datetime

from flask import current_app, request
from app import db
from controller.userTokenController import UserTokenController
from models.userTokenModel import UserToken
from utils import commons, loggings
from utils.response_code import RET, error_map_EN
from utils.rsa_encryption_decryption import RSAEncryptionDecryption
from werkzeug.security import generate_password_hash, check_password_hash


class AdminService(AdminController):

    # 校验密码
    def check_password(self, passwd):
        """
        检验密码的正确性
        :param passwd:  用户登录时填写的原始密码
        :return: 如果正确，返回True， 否则返回False
        """
        return check_password_hash(self.AdminPassword, passwd)

    # 普通管理员登录
    @classmethod
    def admin_login(cls, **kwargs):

        pass_word_admin = kwargs.get('AdminPassword')
        rsa = RSAEncryptionDecryption()
        pass_word_text = rsa.decrypt(pass_word_admin)

        if not pass_word_text:
            return {'code': RET.LOGINERR, 'message': '密码格式不正确', 'error': '密码格式不正确'}

        try:
            filter_list = []
            if kwargs.get('AccountNumber'):
                filter_list.append(cls.Account == kwargs.get('AccountNumber'))

            if not filter_list:
                # return jsonify(code=RET.NODATA, message='参数不完整', error='参数不完整')
                return {'code': RET.NODATA, 'message': '参数不完整', 'error': '参数不完整'}
            filter_list.append(cls.IsDelete == 0)

            admin_info = db.session.query(cls).filter(*filter_list).first()
        except Exception as e:
            return {'code': RET.DBERR, 'message': '获取用户信息失败', 'error': str(e)}

        # 如果无数据，用户不存在
        if not admin_info:
            return {'code': RET.NODATA, 'message': '用户不存在', 'error': '用户不存在'}
            # return jsonify(code=RET.NODATA, message='用户不存在', error='用户不存在')

        # 如果密码错误
        if not admin_info.check_password(pass_word_text):
            # return jsonify(code=RET.PWDERR, message='用户名或密码错误', error='用户名或密码错误')
            return {'code': RET.PWDERR, 'message': '用户名或密码错误', 'error': '用户名或密码错误'}

        # 密码验证成功，生成token
        token = UserTokenController.create_token(admin_info.AdminID, 2)
        expire_time = (datetime.datetime.now() + datetime.timedelta(seconds=current_app.config['TOKEN_EXPIRES'])). \
            strftime('%Y-%m-%d %H:%M:%S')

        try:
            user_token = db.session.query(UserToken).filter(UserToken.AdminID == admin_info.AdminID,
                                                            UserToken.UserType == 2)
        except Exception as e:
            current_app.logger.error(e)

        # 首次登录
        if not user_token.first():
            kwargs = {
                'AdminID': admin_info.AdminID,
                'Token': token,
                'ExpireTime': expire_time,
                'UserType': 2
            }
            user_token_first = UserTokenController.save_token(**kwargs)

            if not user_token_first:
                return {'code': RET.DBERR, 'message': '数据库异常，保存token数据失败', 'error': '数据库异常，保存token数据失败'}

        else:
            last_login_time = commons.query_to_dict(user_token.first()).get('AddTime')
            user_token.update(
                {'Token': token, 'ExpireTime': expire_time, 'LastLoginTime': last_login_time, 'IsValid': 1})
            db.session.commit()

        admin_data = commons.query_to_dict(admin_info)
        db.session.close()
        data_dict = {
            'AccountNumber': admin_data.get('Account'),
            'AdminID': admin_data.get('AdminID'),
            'NickName': admin_data.get('NickName'),
            'Token': token
        }
        # return jsonify(code=RET.OK, message='登录成功', data=data_dict)
        return {'code': RET.OK, 'message': '登录成功', 'data': data_dict}

     # 管理员修改密码
    @classmethod
    def admin_reset(cls, **kwargs):
        try:
            filter_list = []
            filter_list.append(cls.IsDelete == 0)
            filter_list.append(cls.AdminID == kwargs.get('AdminID'))

            admin_info = db.session.query(cls).filter(*filter_list).first()

        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}

        old_password = kwargs.get('AdminPassword')
        new_password = kwargs.get('NewPassword')
        rsa = RSAEncryptionDecryption()
        pass_word_text = rsa.decrypt(old_password)
        new_word_text = rsa.decrypt(new_password)
        print(pass_word_text)
        if admin_info.check_password(pass_word_text):
            kwargs['AdminPassword'] = generate_password_hash(new_word_text)
            del kwargs['NewPassword']
            return AdminController.put(**kwargs)
        else:
            return {'code': RET.NODATA, 'message': '无此账号或原密码错误', 'error': '此账号或原密码错误'}
            # return jsonify(code=RET.NODATA, message='无此账号或原密码错误', error='此账号或原密码错误')
