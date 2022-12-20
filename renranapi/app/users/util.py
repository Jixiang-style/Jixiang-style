#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:renran
@file: util.py
@author: 薛吉祥
@time: 2022/12/15 10:43
@desc:
"""
# 构造jwt登录认证
# 构造header
import datetime
import functools
import os
import sys
import time
from urllib.parse import urlencode
sys.path.append(os.path.abspath(os.path.join(os.getcwd())).split('renranapi')[0])
import jwt
from flask import request, jsonify
from renranapi.app import common
from renranapi.app.models import Users

headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}

# 密钥
SALT = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='

# QQ 登录参数
QQ_APP_ID = '101403367'
QQ_APP_KEY = '93112df14c10d6fde74baa62f5de95ab'
QQ_APP_URI = ''
QQ_APP_CODE = ''


def get_access_token():
    """
    获取access token
    :return:
    """
    params = {
        'grant_type': 'authorization_code',
        'client_id': QQ_APP_ID,
        'client_secret': QQ_APP_KEY,
        'redirect_uri': QQ_APP_URI,
        'code': QQ_APP_CODE
    }

    # urlencode 把字典转换成查询字符串的格式
    url = 'https://graph.qq.com/oauth2.0/token?' + urlencode(params)


def encode_token(user_id, login_time):
    # 构造token
    try:
        payload = {
            'data': {
                'id': user_id,
                'login_time': login_time
            },
            'iat': datetime.datetime.utcnow(),
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),  # 超时时间
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=30)  # 测试30s过期
        }
        result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
        print("加密后", result)

        return result
    except Exception as e:
        return e


def decode_token(token, secret=None):
    """
    检验Token
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    if not secret:
        secret = SALT

    try:
        # payload = jwt.decode(token, secret, algorithms=['HS256'],leeway=datetime.timedelta(seconds=30))  # 用于测试30s过期
        # 不验证过期时间
        payload = jwt.decode(token, secret, algorithms=['HS256'], options={"verify_exp": False})  # 用于测试30s过期
        print("解密后", payload)
        # 验证token中是否包含用户信息
        if 'data' in payload and 'id' in payload['data']:
            return payload
        else:
            return jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:  # 'token认证失败'
        return "token过期"
    except jwt.InvalidKeyError:  # '非法的token'
        return "无效的token"


def authenticate(username):
    """
    用户登录，登录成功返回token，将登录时间写入数据库；失败返回失败原因
    :param username:
    :param password:
    :return:
    """
    # 验证账号密码，正确则返回token，用于后续接口权限验证
    # 查询数据库，是否有满足条件的用户
    user_db_info = Users.query.filter_by(nickname=username).first()
    print("数据库查询，第一条数据", user_db_info)
    if user_db_info:
        print("登录成功！")
        login_time = int(time.time())
        user_db_info.login_time = login_time
        # todo token写进数据库
        Users.update(Users)
        token = encode_token(user_db_info.id, login_time)
        return jsonify(common.trueReturn(token, "登录成功"))
    else:
        return jsonify(common.falseReturn("", "登录失败", 401))


def identify(f):
    """
    用户鉴权
    让装饰器装饰的函数属性不会变 -- name属性
    第1种方法,使用functools模块的wraps装饰内部函数
    :param f:
    :return:
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            # 获取请求头中authorization
            auth_header = request.headers.get('Authorization')
            print("获取到的请求头是：", auth_header)
            if auth_header:
                auth_token_arr = auth_header.split(" ")
                print(auth_token_arr)
                if not auth_token_arr or auth_token_arr[0] != 'JWT' or len(auth_token_arr) != 2:
                    result = common.falseReturn("", "请传递正确的验证头信息")
                else:
                    auth_token = auth_token_arr[1]
                    payload = decode_token(auth_token)
                    print("payload", payload)
                    if isinstance(payload, dict):
                        user = Users.get(Users, id=payload["data"]["id"])
                        if not user:
                            result = common.falseReturn("", "查询不到用户信息")
                        else:
                            if int(user.login_time) == payload['data']["login_time"]:
                                result = common.trueReturn(user.id, "请求成功")
                            else:
                                result = common.falseReturn("", "Token已过期，请重新登录")
                    else:
                        result = common.falseReturn(payload, "token格式有误！")
            else:
                result = common.falseReturn("", "Token缺失")
            return result
        except PermissionError:
            return {'code': 4001, 'message': '请先登录认证.'}, 401

    '第2种方法,在返回内部函数之前,先修改wrapper的name属性'
    # wrapper.__name__ = f.__name__
    return wrapper
