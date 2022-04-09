# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Admin(db.Model):
    __tablename__ = 'admin'

    AutoID = db.Column(db.BigInteger, primary_key=True, info='自增ID')
    AdminID = db.Column(db.String(255), info='管理员ID')
    NickName = db.Column(db.String(255), info='管理员昵称')
    Account = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='管理员账号')
    AdminPassword = db.Column(db.String(2000, 'utf8mb4_0900_ai_ci'), info='管理员密码')
    CreateTime = db.Column(db.DateTime, info='创建时间')
    IsDelete = db.Column(db.Integer, info='表示该数据是否有效：0--有效；1--无效')
