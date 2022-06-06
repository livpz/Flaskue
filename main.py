from flask import Flask, redirect, url_for

class App(object):
    app = None
    def __ini__(self):
        pass

    @classmethod
    def build_app(cls):
        cls.app = Flask(__name__)
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




