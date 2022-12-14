#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:renran
@file: config.py
@author: 薛吉祥
@time: 2022/12/14 16:31
@desc:
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 初始化
app = Flask(import_name=__name__, template_folder='templates')


# 声明和加载配置
class Config(object):
    DEBUG = True
    # 数据库链接配置 = 数据库名称://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称?charset=编码类型
    SQLALCHEMY_DATABASE_URI = "mysql://root:123@127.0.0.1:3306/students?charset=utf8"
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 显示原始SQL语句
    SQLALCHEMY_ECHO = True


app.config.from_object(Config)

# 初始化SQLAlchemy
db = SQLAlchemy()  # 初始化数据库操作对象
db.init_app(app)  # 初始化数据库链接


class Users(db.Model):
    # 表结构声明
    __tablename__ = "tb_suers"

    # 字段声明
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    mobile = db.Column(db.String(64), index=True, comment="手机号码")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    age = db.Column(db.SmallInteger, nullable=True, comment="年龄")
    alipay = db.Column(db.String(128), unique=True, comment="支付宝号码")
    wxchat = db.Column(db.String(128), unique=True, comment="微信号码")
    qq_number = db.Column(db.String(128), unique=True, comment="QQ号码")
    # 用户账户信息
    nickname = db.Column(db.String(64), nullable=True, comment="用户昵称")
    # todo 头像文件待处理
    avatar = db.Column(db.String(128), unique=True, comment="用户头像")
    money = db.Column(db.Numeric(8, 2), default=0, comment="钱包")

    # 自定义方法
    def __repr__(self):
        return 'User:%s' % self.name


class Teacher(db.Model):
    # 表结构声明
    __tablename__ = 'tb_teacher'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    option = db.Column(db.Enum("讲师", "助教", "班主任"), default="讲师")

    def __repr__(self):
        return 'Teacher:%s' % self.name


class Course(db.Model):
    # 定义表名
    __tablename__ = 'tb_course'
    # 定义字段对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.Numeric(6, 2))

    # repr()方法类似于django的__str__，用于打印模型对象时显示的字符串信息
    def __repr__(self):
        return 'Course:%s' % self.name


@app.route(rule='/')
def index():
    return "ok"


if __name__ == '__main__':
    # 创建所有的数据表/删除所有表
    # 创建过之后注释掉就可以了
    with app.app_context():
        db.create_all()  # 创建表
    #     db.drop_all()  # 删除所有表
    # 运行flask
    app.run(debug=True)
