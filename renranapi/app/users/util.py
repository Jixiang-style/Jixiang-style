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

import jwt
from flask import current_app, g

headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}

# 密钥
SALT = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='


def create_token(username, password):
    # 构造payload
    payload = {
        'username': username,
        'password': password,  # 自定义用户ID
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 超时时间
    }
    result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
    print("加密后", result)

    return result


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    if not secret:
        secret = current_app.config['JWT_SECRET']

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        print("解密后", payload)
        return payload
    except jwt.InvalidTokenError:  # 'token已失效'
        return 1
    except jwt.InvalidSignatureError:  # 'token认证失败'
        return 2
    except jwt.InvalidKeyError:  # '非法的token'
        return 3


def login_required(f):
    """
    让装饰器装饰的函数属性不会变 -- name属性
    第1种方法,使用functools模块的wraps装饰内部函数
    :param f:
    :return:
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            print(11111111)
            print("g.username为：", g.username)
            print("g为：", g)
            if g.username == 1:
                return {'code': 4001, 'message': 'token已失效'}, 401
            elif g.username == 2:
                return {'code': 4001, 'message': 'token认证失败'}, 401
            elif g.username == 2:
                return {'code': 4001, 'message': '非法的token'}, 401
            else:
                return f(*args, **kwargs)
        except BaseException:
            return {'code': 4001, 'message': '请先登录认证.'}, 401

    '第2种方法,在返回内部函数之前,先修改wrapper的name属性'
    # wrapper.__name__ = f.__name__
    return wrapper
