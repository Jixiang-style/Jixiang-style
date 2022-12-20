from flask import Flask
from flask import jsonify
from flask_cors import CORS

# 初始化
app = Flask(import_name=__name__, template_folder='templates')
cors = CORS(app, supports_credentials=True)  # 配置全局路由


# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
@app.route('/getMsg', methods=['GET', 'POST'])
def home():
    response = {
        'msg': 'Hello, Python !'
    }
    return jsonify(response)


# 启动运行
# if __name__ == '__main__':
#     app.run(debug=True)  # 这样子会直接运行在本地服务器，也即是 localhost:5000
# app.run(host='your_ip_address') # 这里可通过 host 指定在公网IP上运行
