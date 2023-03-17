#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:renran
@file: common.py
@author: 薛吉祥
@time: 2022/12/15 18:06
@desc:
"""

# 腾讯防水墙配置
TENCENT_CAPTCHA = {
    "GATEWAY": "https://ssl.captcha.qq.com/ticket/verify",
    "APPID": "2072894469",
    "App_Secret_Key": "0vcR-k9wMOk1SArX_gvB7qQ**",
}

# QQ 登录参数
QQ_APP_ID = '101403367'
QQ_APP_KEY = '93112df14c10d6fde74baa62f5de95ab'
QQ_APP_URI = 'http://127.0.0.1:8070/oauth_callback.html'
QQ_STATE = '/'


def trueReturn(data, msg):
    return {
        "code": 200,
        "status": True,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg, code=None):
    return {
        "code": code,
        "status": False,
        "data": data,
        "msg": msg
    }
