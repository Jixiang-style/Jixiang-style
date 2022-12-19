#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:renran
@file: view.py
@author: 薛吉祥
@time: 2022/12/14 16:28
@desc:
"""
import time

import jwt
from flask import g, request, Flask, jsonify
from util import SALT
from util import encode_token, identify, authenticate
from renranapi.app.models import app, Users, DB, UsersInfo
from renranapi.app import common
from renranapi.app.users import sms, connect

# app = Flask(__name__)

# 处理中文编码
app.config['JSON_AS_ASCII'] = False


# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)


@app.before_request
def jwt_authentication():
    """
    1.获取请求头Authorization中的token
    2.判断是否以 Bearer开头
    3.使用jwt模块进行校验
    4.判断校验结果,成功就提取token中的载荷信息,赋值给g对象保存
    """
    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Bearer '):
        "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符"
        token = auth[7:]
        "校验token"
        g.username = None
        try:
            "判断token的校验结果"
            payload = jwt.decode(token, SALT, algorithms=['HS256'])
            "获取载荷中的信息赋值给g对象"
            g.username = payload.get('username')
        except jwt.ExpiredSignatureError:  # 'token已失效'
            g.username = 1
        except jwt.DecodeError:  # 'token认证失败'
            g.username = 2
        except jwt.InvalidTokenError:  # '非法的token'
            g.username = 3


@app.route('/')
def hello_world():
    return "ok"


# 登录
# todo qq登录
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        type_ = data.get("type")
        if type_ == 'login':
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                return jsonify(common.falseReturn("", "登陆失败，请检查用户名密码是否正确"))
            else:
                return authenticate(username)
        else:
            return {"code": 201, "message": "type is false"}

    elif request.method == 'GET':
        return {"code": 202, "message": "get is nothing"}
    else:
        return {"code": 203, "message": "'not support other method'"}


# 注册
# # todo 短信、qq邮箱接收短信
# @app.route('/api/register', methods=['post'])
# def register():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     user = Users(nickname=username, password=Users.set_password(Users, password), login_time=int(time.time()))
#     Users.add(Users, user)
#     if user.id:
#         returnUser = {
#             'id': user.id,
#             'nickname': user.nickname,
#             'login_time': user.login_time
#         }
#         return jsonify(common.trueReturn(returnUser, "用户注册成功"))
#     else:
#         return jsonify(common.falseReturn("", "用户注册失败"))


# 注册
# todo 短信、qq邮箱接收短信
@app.route('/api/register', methods=['post', 'get'])
def register():
    phone_number = request.form.get("phoneNumber")
    yz_code = request.form.get("yz_code")
    print("接口收到的验证码", yz_code, type(yz_code))
    # 检查改手机号是否注册过
    db_umber = DB(UsersInfo).get(mobile=phone_number)
    if db_umber:
        return jsonify(common.falseReturn("", "该号码已经被注册"))
    # 连接redis，获取验证码
    conn = connect.redisConnect(1)
    if conn.get(phone_number) == 0:
        return jsonify(common.falseReturn("", "验证码已过期"))
    rds_code = conn.get(phone_number)
    if rds_code is None:
        return jsonify(common.falseReturn("", "验证码为空"))
    # bytes 类型转字符串
    rds_code = str(rds_code, "utf-8")
    print("表单收到的验证码 %s %s \n redis收到的验证码%s %s" % (yz_code, type(yz_code), rds_code, type(rds_code)))
    if rds_code == yz_code:
        user_info = UsersInfo(mobile=phone_number)
        DB(UsersInfo).add(user_info)
        return jsonify(common.trueReturn("", "注册成功!!!"))
    else:
        return jsonify(common.falseReturn("", "验证码有误"))


# 获取短信验证码
@app.route("/api/send_code", methods=["get", "post"])
def send_code():
    phone_number = request.form.get("phoneNumber")
    # 发送短信验证码
    sms_code = sms.generate_code()
    # todo 暂时同步发送，后续用celery改异步
    sms.send_message(sms_code, phone_number)
    # 同步写进redis
    conn = connect.redisConnect(1)
    # 默认保留五分钟
    conn.setex(phone_number, 300, sms_code)
    print("收到redis验证码", conn.get(phone_number))
    return jsonify(common.trueReturn(1, "success"))


# 获取用户信息
@app.route("/api/user", methods=["get"])
def get():
    a = DB(Users).get(id=5)
    # DB(Users).delete(id=3)
    user = Users(nickname="user002", password=Users.set_password(Users, "123456"), login_time=int(time.time()))
    DB(Users).add(user)
    print("a:", a)
    return "操作成功！！！"


# 测试接口
@app.route('/api/test', methods=['GET', 'POST'])
@identify
def submit_test_info_():
    username = g.username
    return username


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)
