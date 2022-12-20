#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:renran
@file: connect.py
@author: 薛吉祥
@time: 2022/12/16 17:26
@desc:
"""
# redis配置
import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379


# 生产要配置redis密码认证，避免redis裸奔
# REDIS_AUTH = 123456


def redisConnect(dbNum):
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=dbNum)
    conn = redis.Redis(connection_pool=pool)
    # conn.setex("123456", 300, "654321")
    return conn

# 测试链接redis
# redisConnect(1)
