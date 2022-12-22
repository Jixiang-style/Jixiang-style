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
from urllib.parse import urlencode

import jwt
import requests
from flask import g, request, jsonify
from util import SALT
from util import identify, authenticate
from renranapi.manage import app
from renranapi.app.models import Users, DB, UsersInfo
from renranapi.app import common
from renranapi.app.users import sms, connect

# app = Flask(__name__)

# 处理中文编码
app.config['JSON_AS_ASCII'] = False


# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
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
        data = request.json
        print("登录获取到的数据是", data)
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify(common.falseReturn("", "登陆失败，请检查用户名密码是否正确"))
        else:
            return authenticate(username, password)
    elif request.method == 'GET':
        return {"code": 202, "message": "get is nothing"}
    else:
        return {"code": 203, "message": "'not support other method'"}


# 腾讯防水墙(todo 还有问题，待排查)
@app.route('/api/captcha', methods=['GET', 'POST'])
def captcha():
    if request.method == 'POST':
        data = request.json
        print("防水墙获取到的数据是", data)
        # 获取票据信息
        ret = request.json.get("ret")
        rand_str = request.json.get("randstr")
        ticket = request.json.get("ticket")
        ip = request.remote_addr
        # 检查票据信息
        check_ret = check_robot(ticket, rand_str, ip)
        check_ret.update({"ret": ret, "rand_str": rand_str, "ticket": ticket, "ip": ip})
        print("检查票据", check_ret)
        return jsonify(common.trueReturn({"message": True, "randstr": rand_str}, "防水墙验证成功").get("data"))


# 轮播图(todo 先写在本地，后续同步到数据库)
@app.route('/api/banner', methods=['GET', 'POST'])
def banner():
    if request.method == 'GET':
        banner_base_url = "/Users/Jixiang/PycharmProjects/pythonProject/project/renran/renranapi/uploads/banner/"
        banner_base_url = "/static/image/"
        banners = dict()
        banners['data'] = list()
        for i in range(4):
            banners['data'].append({"image": i, "link": banner_base_url + "%d.jpg" % (i + 1)})
        print(banners)
        # data = request.json
        # print("防水墙获取到的数据是", data)
        # # 获取票据信息
        # ret = request.json.get("ret")
        # rand_str = request.json.get("randstr")
        # ticket = request.json.get("ticket")
        # ip = request.remote_addr
        # # 检查票据信息
        # check_ret = check_robot(ticket, rand_str, ip)
        # check_ret.update({"ret": ret, "rand_str": rand_str, "ticket": ticket, "ip": ip})
        # print("检查票据", check_ret)
        return jsonify(banners)


# 检查票据信息
def check_robot(ticket, rand_str, user_ip):
    url = "https://ssl.captcha.qq.com/ticket/verify"
    """
    aid (必填)	2032405422
    AppSecretKey (必填)	04urfsEZJDbinsshD1hDlPw**
    Ticket (必填)	验证码客户端验证回调的票据
    Randstr (必填)	验证码客户端验证回调的随机串
    UserIP (必填)	提交验证的用户的IP地址（eg: 10.127.10.2）
    """
    params = {
        "aid": common.TENCENT_CAPTCHA.get("APPID"),
        "AppSecretKey": common.TENCENT_CAPTCHA.get("App_Secret_Key"),
        "Ticket": ticket,
        "Randstr": rand_str,
        "UserIP": user_ip
    }

    response = requests.get(url, params=params, verify=False)

    return response.json()


# todo qq登录暂时无法实现，需要注册企业资质
@app.route('/api/oauth/qq/url', methods=['post', 'get'])
def qq_auth():
    print("即将获取qq登录地址")
    # 获取qq登录地址
    params = {
        'response_type': 'code',
        'client_id': common.QQ_APP_ID,
        'redirect_uri': common.QQ_APP_URI,
        'state': common.QQ_STATE,
        'scope': 'get_user_info',
    }

    url = "https://graph.qq.com/oauth2.0/authorize?" + urlencode(params)
    print(url)
    return jsonify(common.trueReturn(url, "返回qq登录地址成功").get("data"))


@app.route('/api/register', methods=['post', 'get'])
def register():
    # 获取结构体信息
    phone_number = request.json.get("mobile")
    nickname = request.json.get("nickname")
    password = request.json.get("password")
    print("收到的参数", request.json)
    yz_code = request.json.get("sms_code")
    print("接口收到的验证码", yz_code, type(yz_code))
    # 检查改手机号是否注册过
    db_umber = DB(Users).get(mobile=phone_number)
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
        user = Users(nickname=nickname, mobile=phone_number, password=Users.set_password(Users, password),
                     login_time=str(time.time()))
        DB(Users).add(user)
        auth_data = authenticate(phone_number, password).json
        data = {"token": auth_data.get("token"), "nickname": user.nickname, "id": user.id,
                "username": user.mobile}
        return jsonify(common.trueReturn(data, "注册成功!!!").get("data"))
    else:
        return jsonify(common.falseReturn("", "验证码有误"))


# 获取短信验证码
@app.route("/api/send_code", methods=["get", "post"])
def send_code():
    if request.method == "POST":
        phone_number = request.json.get("phoneNumber")
        print("结构体", request.json)
        print("收到的电话号码", phone_number)
        # 发送短信验证码
        sms_code = sms.generate_code()
        # todo 暂时同步发送，后续用celery改异步
        sms.send_message(sms_code, phone_number)
        print("验证码已发送")
        # 同步写进redis
        conn = connect.redisConnect(1)
        print("redis连接成功")
        # 默认保留五分钟
        conn.setex(phone_number, 300, sms_code)
        print("收到redis验证码", conn.get(phone_number))
        return jsonify(common.trueReturn(1, "success"))
    if request.method == "GET":
        return jsonify(common.falseReturn("", "请求方法错误!!!"))


# 获取用户信息
@app.route("/api/user", methods=["get"])
def get():
    a = DB(Users).get(id=5)
    # DB(Users).delete(id=3)
    user = Users(nickname="user002", password=Users.set_password(Users, "123456"))
    # DB(Users).add(user)
    print("a:", user)
    return "操作成功！！！"


# 测试接口
@app.route('/api/test', methods=['GET', 'POST'])
@identify
def submit_test_info_():
    username = g.username
    return username


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
