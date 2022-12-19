#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:renran
@file: common.py
@author: 薛吉祥
@time: 2022/12/15 18:06
@desc:
"""


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
