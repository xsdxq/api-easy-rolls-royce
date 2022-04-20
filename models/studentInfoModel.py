# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class StudentInfo(db.Model):
    __tablename__ = 'student_info'

    AutoID = db.Column(db.BigInteger,  server_default=db.FetchedValue(),primary_key=True)
    StudentID = db.Column(db.String(25))
    Class = db.Column(db.String(25))
    Grade = db.Column(db.String(25))
    Name = db.Column(db.String(25))
