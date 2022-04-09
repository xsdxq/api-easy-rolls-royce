# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Batch(db.Model):
    __tablename__ = 'Batch'

    AutoID = db.Column(db.BigInteger, primary_key=True, info='自增ID')
    BatchID = db.Column(db.BigInteger, info='批次ID')
    Year = db.Column(db.String(8, 'utf8mb4_0900_ai_ci'), info='年份')
    Term = db.Column(db.String(2, 'utf8mb4_0900_ai_ci'), info='学期：1 or 2')
    Week = db.Column(db.String(5, 'utf8mb4_0900_ai_ci'), info='周次')
    IsCurrent = db.Column(db.Integer, info='是否最新周次：1-是；0-否')
    IsDelete = db.Column(db.Integer, info='是否删除:1-是；0-否')
