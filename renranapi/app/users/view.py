#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:renran
@file: view.py
@author: 薛吉祥
@time: 2022/12/14 16:28
@desc:
"""
import jwt
from flask import g, request, Flask
from util import SALT
from util import create_token, login_required
from renranapi.app.models import app, db, Users

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
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        type_ = data.get("type")
        if type_ == 'login':
            username = data.get("username")
            password = data.get("password")
            # 验证账号密码，正确则返回token，用于后续接口权限验证
            # 查询数据库，是否有满足条件的用户
            db_info = Users.query.filter_by(nickname=username, password=password).first()
            print("数据库查询，第一条数据", db_info)
            if db_info:
                print("登录成功！")
                token = create_token(username, password)
                return {"code": 200, "message": "success", "data": {"token": token}}
            # if username == "root" and password == "123456":
            #     token = create_token(username, password)
            #     return {"code": 200, "message": "success", "data": {"token": token}}
            else:
                return {"code": 501, "message": "登陆失败"}
        else:
            return {"code": 201, "message": "type is false"}

    elif request.method == 'GET':
        return {"code": 202, "message": "get is nothing"}
    else:
        return {"code": 203, "message": "'not support other method'"}


# 测试接口
@app.route('/api/test', methods=['GET', 'POST'])
@login_required
def submit_test_info_():
    username = g.username
    return username


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)
