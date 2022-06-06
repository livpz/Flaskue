from operator import index
from flask import Blueprint, render_template
from .config import PageMap


index_bp = Blueprint('index', __name__,
                    static_folder='./static/',
                    template_folder='./templates/',
                    url_prefix='/index/')

@index_bp.route('/')
def index():
    return render_template(PageMap.index)

