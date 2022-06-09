from operator import index
from flask import Blueprint, redirect, render_template, request, session, url_for
from .config import PageMap


index_bp = Blueprint('index', __name__,
                    static_folder='./static/',
                    template_folder='./templates/',
                    url_prefix='/index/')

@index_bp.route('/')
def index():
    pw = request.args.get('pw')
    if pw == "yby":
        session['login'] = True
    return render_template(PageMap.index)

@index_bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index.index'))


