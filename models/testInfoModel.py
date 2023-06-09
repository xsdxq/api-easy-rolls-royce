# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class TestInfo(db.Model):
    __tablename__ = 'test_info'

    AutoID = db.Column(db.BigInteger, primary_key=True, info='自增ID')
    RecordID = db.Column(db.String(25), info='记录ID')
    BatchID = db.Column(db.String(25), info='批次ID')
    StudentID = db.Column(db.String(25, 'utf8mb4_0900_ai_ci'), info='学生学号')
    Grade = db.Column(db.String(25), info='学生年级')
    Class = db.Column(db.String(25), info='学生班级')
    Name = db.Column(db.String(25), info='学生姓名')
    NameInImage = db.Column(db.String(255), info='识别出的姓名')
    TestTime = db.Column(db.String(255), info='检测时间')
    ImageUrl = db.Column(db.String(2000), info='上传截图url')
    NameTest = db.Column(db.Integer, server_default=db.FetchedValue(), info='姓名校验是否通过 0--通过 1--没通过')
    TestResults = db.Column(db.String(25), info='检测结果')
    CreateTime = db.Column(db.DateTime, server_default=db.FetchedValue(),info='创建时间')
    IsDelete = db.Column(db.Integer, server_default=db.FetchedValue(),info='标志该条数据是否有效: 0--表示有效,1--无效')
