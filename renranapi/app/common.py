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
