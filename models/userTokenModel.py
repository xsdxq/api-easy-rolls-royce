# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class UserToken(db.Model):
    __tablename__ = 'user_token'

    AutoID = db.Column(db.BigInteger, primary_key=True, info='自增id')
    AdminID = db.Column(db.String(22, 'utf8mb4_0900_ai_ci'), index=True, info='登录的用户ID')
    UserType = db.Column(db.Integer, server_default=db.FetchedValue(), info='用户类别：1--平台用户  2--管理员')
    Token = db.Column(db.String(255, 'utf8_general_ci'), info='登录的toke令牌')
    ExpireTime = db.Column(db.DateTime, info='token过期时间')
    LoginIP = db.Column(db.String(255, 'utf8_general_ci'), info='登录IP')
    LastLoginTime = db.Column(db.DateTime, info='最后一次登录时间')
    IsValid = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否有效；0--无效；1--有效；  系统管理员临时控制位')
    AddTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')
