#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:renran
@file: config.py
@author: 薛吉祥
@time: 2022/12/14 16:31
@desc:
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from renranapi.manage import app
import pymysql

pymysql.install_as_MySQLdb()


# 声明和加载配置
class Config(object):
    DEBUG = True
    # 数据库链接配置 = 数据库名称://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称?charset=编码类型
    SQLALCHEMY_DATABASE_URI = "mysql://root@127.0.0.1:3306/renran_test?charset=utf8"
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 显示原始SQL语句
    SQLALCHEMY_ECHO = True


app.config.from_object(Config)

# 初始化SQLAlchemy
db = SQLAlchemy()  # 初始化数据库操作对象
db.init_app(app)  # 初始化数据库链接


class UsersInfo(db.Model):
    # 表结构声明
    __tablename__ = "tb_usersInfo"

    # 字段声明
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    user_id = db.Column(db.String(64), index=True, comment="用户身份标识")
    mobile = db.Column(db.String(64), index=True, comment="手机号码")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    age = db.Column(db.SmallInteger, nullable=True, comment="年龄")
    alipay = db.Column(db.String(128), unique=True, comment="支付宝号码")
    wxchat = db.Column(db.String(128), unique=True, comment="微信号码")
    qq_number = db.Column(db.String(128), unique=True, comment="QQ号码")
    # todo 头像文件待处理
    avatar = db.Column(db.String(128), unique=True, comment="用户头像")
    money = db.Column(db.Numeric(8, 2), default=0, comment="钱包")

    # 自定义方法
    def __repr__(self):
        return 'User:%s' % self.user_id


class Users(db.Model):
    # 表结构声明
    __tablename__ = "tb_users"

    # 字段声明
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    # 用户账户信息
    nickname = db.Column(db.String(64), nullable=True, unique=True, comment="用户昵称")
    mobile = db.Column(db.String(64), index=True, comment="手机号码")
    password = db.Column(db.String(128), nullable=True, comment="密码")
    login_time = db.Column(db.String(128), default=0, comment="登录时间")

    # 设置密码
    def set_password(self, password):
        return generate_password_hash(password)

    # 校验密码
    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    # 查询用户
    def get(self, id):
        return self.db.query.filter_by(id=id).first()

    # 添加用户
    def add(self, user):
        db.session.add(user)
        return session_commit()
        # 自定义方法

    # 更新
    def update(self):
        return session_commit()

    # 删除
    def delete(self, id):
        self.db.query.filter_by(id=id).delete()
        return session_commit()

    def __repr__(self):
        return 'User:%s' % self.nickname


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


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        return str(e)


class DB(object):

    def __init__(self, db):
        self.db = db

    # 查询用户
    def get(self, *args, **kwargs):
        return self.db.query.filter_by(*args, **kwargs).first()

    # 添加用户
    def add(self, *args, **kwargs):
        db.session.add(*args, **kwargs)
        return session_commit()
        # 自定义方法

    # 更新
    def update(self):
        return session_commit()

    # 删除
    def delete(self, *args, **kwargs):
        self.db.query.filter_by(*args, **kwargs).delete()
        return session_commit()


# class Role(db.Model):
#     """用户角色/身份表"""
#     # 重命名表名
#     __tablename__ = "tb_roles"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(32), unique=True)
#     # 这个重点介绍一下，这是额外添加的一个属性，并不会添加在表里面
#     users = db.relationship("User", backref="role")
#
#     def __repr__(self):
#         """定义之后，可以让显示对象的时候更直观"""
#         return "Role object: name=%s" % self.name


@app.route(rule='/')
def index():
    return "ok"

# if __name__ == '__main__':
# 创建/删除所有的表
#     with app.app_context():
#         db.create_all()  # 创建表
#     us3 = Users(nickname='张三', password='123456', login_time=int(time.time()))
#     us4 = Users(nickname='李四', password='123456', login_time=int(time.time()))
#     us5 = Users(nickname='admin', password='123456', login_time=int(time.time()))
#
#     # 一次保存多条数据
#     db.session.add_all([us5, us3, us4])
#     db.session.commit()
#     # 删除表
#         db.drop_all()

# 创建对象
# role1 = Role(name="admin")
# session记录对象任务
# db.session.add(role1)
# 提交任务到数据库中
# db.session.commit()
#
# role2 = Role(name="stuff")
# db.session.add(role2)
# db.session.commit()

# us1 = Users(name='wang', email='wang@163.com', password='123456', role_id=role1.id)
# us2 = Users(name='zhang', email='zhang@189.com', password='201512', role_id=role2.id)
# us3 = Users(name='chen', email='chen@126.com', password='987654', role_id=role2.id)
# us4 = Users(name='zhou', email='zhou@163.com', password='456789', role_id=role1.id)

# 运行flask
# app.run(debug=True)
