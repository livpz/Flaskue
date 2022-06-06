import json
import sqlite3 as sql
import uuid
from flask import Blueprint, render_template, request
from .config import PageMap, DB

post_bp = Blueprint('post',
                     __name__,
                     url_prefix='/post/',
                     template_folder='./templates',
                     static_folder='./static')

@post_bp.route('/page/')
def post_page():
    _post_id = request.args.get('post_id')
    return render_template(PageMap.post, post_id=_post_id)

@post_bp.route('/get_post_list/')
def get_post_list():
    index = request.args.get('index')
    index = index if index else 1
    index = (int(index) - 1)*10 -1
    with sql.connect(DB.sqlite) as conn:
        cur = conn.cursor()
        SQL_SUM = "SELECT COUNT(id) FROM post"
        cur.execute(SQL_SUM)
        blog_sum = cur.fetchone()
        print('count:', blog_sum)
        page_sum = blog_sum[0]//10 + 1
        SQL_LIMIT = f"SELECT title, tags, date, view, id FROM post order by date DESC LIMIT 10 offset {index}"
        cur.execute(SQL_LIMIT)
        res = cur.fetchall()

    res = zip(range(len(res)), res)
    RESPONSE = {
        "page_sum": page_sum,
        "post_list" :{ x[0]: {
            'title': x[1][0],
            'tags': x[1][1],
            'date': x[1][2],
            'view': x[1][3],
            'id': x[1][4]
        } for x in res
       }
    }
    print("RESPONSE:", RESPONSE)
    return RESPONSE


@post_bp.route('/get_post/')
def get_post():
    _post_id = request.args.get('post_id')
    print('_post_id:', _post_id)
    with sql.connect(DB.sqlite) as conn:
        cur = conn.cursor()
        SQL = """SELECT title, tags, date, view, content FROM post
        INNER JOIN content
        ON post.id = content.id
        WHERE post.id = '{}'
        """.format(_post_id)
        cur.execute(SQL)
        res = cur.fetchone()

    RESPONSE = {
        'title' : res[0],
        'tags': res[1],
        'date': res[2],
        'view_count': res[3],
        'content': res[4]
    }
    return RESPONSE


@post_bp.route('/write/')
def write():
    _post_id = request.args.get('post_id')
    if not _post_id:
        _post_id = ''
    return render_template(PageMap.write,post_id=_post_id)


@post_bp.route('/upload/', methods=['POST'])
def upload():
    jsondata = request.get_data() # 此时格式为byte
    jsondata = jsondata.decode("utf-8") # 解码
    jsondata = json.loads(jsondata) # 类型转换 string to dict
    print(jsondata)
    title = jsondata['title']
    tags = jsondata['tags']
    date = jsondata['date']
    content = jsondata['content']
    id = jsondata['id']
    if id == '':
        id = uuid.uuid4()
    with sql.connect(DB.sqlite) as conn:
        cur = conn.cursor()

        SQL = """INSERT OR REPLACE INTO post (
            id, title, tags, date, view
        ) VALUES(
            '{}', '{}', '{}', '{}', '{}'
        )
        """.format(id, title, tags, date, 0)
        cur.execute(SQL)

        SQL_CONTENT = """INSERT OR REPLACE INTO content(id, content) VALUES(
            '{}', '{}'
        )""".format(id,content)
        cur.execute(SQL_CONTENT)
        conn.commit()

    return '上传成功'