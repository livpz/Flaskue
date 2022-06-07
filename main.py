from flask import Flask, redirect, url_for
from datetime import timedelta

class App(object):
    app = None
    def __ini__(self):
        pass

    @classmethod
    def build_app(cls):
        cls.app = Flask(__name__)
        cls.app.config['SECRET_KEY'] = '5da28c75-1199-49f7-a4db-bb9db1d6a6a3'
        cls.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1) # 设置为1小时候过期
        app = cls.app
        @app.route('/')
        def index():
            return redirect(url_for('index.index'))


    @classmethod
    def get_app(cls):
        return cls.app

    @classmethod
    def run_app(cls):
        cls.app.run(host= '127.0.0.1', port=5000)




