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
        "status": True,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }
