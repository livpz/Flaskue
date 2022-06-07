import re
from flask import session, url_for, redirect


def logging(level):
    def outwrapper(func):
        def wrapper(*args, **kwargs):
            print("[{0}]: enter {1}()".format(level, func.__name__))
            return func(*args, **kwargs)
        return wrapper
    return outwrapper



def if_login(func):
    def wrapper(*args, **kwargs):
        print("SESSION :", session.get('login'))
        if session.get('login'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index.index'))
    return wrapper