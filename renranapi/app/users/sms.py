#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:renran
@file: sms.py
@author: 薛吉祥
@time: 2022/12/16 16:49
@desc:
"""
# 容联云配置
import random

from ronglian_sms_sdk import SmsSDK

accId = '8a216da87051c90f0170a5fd83a52c8c'
accToken = '0650996bf68943238922e578f7efb0b4'
appId = '8a216da87051c90f0170a5fd84102c93'


def generate_code():
    verificationCode = ""
    for i in range(6):
        intNum = random.randint(0, 9)
        verificationCode += str(intNum)
    return verificationCode


def send_message(sms_code, mobile, expire_time=60):
    sdk = SmsSDK(accId, accToken, appId)
    print(sdk)
    tid = '1'
    datas = ('%s' % sms_code, '%s' % expire_time)
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)

# send_message(generate_code(), "13026330376")
