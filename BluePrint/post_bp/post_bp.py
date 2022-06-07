import json
import sqlite3 as sql
import uuid
import markdown
from flask import Blueprint, redirect, render_template, request, session
from .config import PageMap, DB
from Tools import if_login
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
        SQL_LIMIT = f"SELECT title, tags, date, view, post.id FROM post LEFT JOIN ip ON ip.id = post.id WHERE show == 1 order by date DESC  LIMIT 10 offset {index}"
        cur.execute(SQL_LIMIT)
        res = cur.fetchall()

    def hot(view):
        hot = "/index/static/img/hot_base.png"
        if int(view) > 50:
            hot = "/index/static/img/hot_mid.png"
        if int(view) > 100:
            hot = "/index/static/img/hot_top.png"
        return hot

    def icon(tags):
        tags = tags.split('/')
        icon = {
            'python': '/index/static/img/icon_python.png',
            'vue': '/index/static/img/icon_vue.png',
            'flask': '/index/static/img/icon_flask.png'
        }
        out = [
            {
                'icon' if icon.get(i) else 'text': icon.get(i) if icon.get(i) else i
            } for i in tags
        ]
        return out

    res = zip(range(len(res)), res)
    RESPONSE = {
        "page_sum": page_sum,
        "post_list" :{ x[0]: {
            'title': x[1][0],
            'tags': icon(x[1][1]),
            'date': x[1][2][5:],
            'view': x[1][3],
            'id': x[1][4],
            'hot': hot(x[1][3])
        } for x in res
       }
    }
    print("RESPONSE:", RESPONSE)
    return RESPONSE


@post_bp.route('/get_post/')
def get_post():
    _post_id = request.args.get('post_id')
    edit = request.args.get('edit')
    ip = request.remote_addr

    with sql.connect(DB.sqlite) as conn:
        cur = conn.cursor()
        # SQL = """SELECT title, tags, date, view, content, ip  FROM post
        # INNER JOIN content INNER JOIN ip
        # ON post.id = content.id ON post.id = ip.id
        # WHERE post.id = '{}'
        # """.format(_post_id)

        SQL ="""SELECT title, tags, date, view, content, ip
        FROM (post LEFT JOIN content
        ON post.id = post.id )
        LEFT JOIN ip  ON ip.id = post.id
        WHERE post.id = '{}';""".format(_post_id)

        cur.execute(SQL)
        res = cur.fetchone()

        ip_string = res[5]
        view_count = res[3]
        set_ip = set(ip_string.split('#'))
        if ip not in set_ip:
            view_count += 1
            ip_string += '#' + ip
        SQL_IP = f"UPDATE ip SET ip = '{ip_string}',view='{view_count}' WHERE id = '{_post_id}' "
        cur.execute(SQL_IP)
        conn.commit()
    if edit:
        _content = res[4]
    else:
        _content = markdown.markdown(res[4])

    RESPONSE = {
        'title' : res[0],
        'tags': res[1],
        'date': res[2],
        'view_count': view_count,
        'content': _content
    }
    return RESPONSE


@post_bp.route('/write/')
@if_login
def write():
    _post_id = request.args.get('post_id')
    if not _post_id:
        _post_id = ''
    return render_template(PageMap.write, post_id=_post_id)

@post_bp.route('/tomd/', methods=['POST'])
def toMD():
    if not session.get('login'):
        return 'Permission denied'
    jsondata = request.get_data() # 此时格式为byte
    jsondata = jsondata.decode("utf-8") # 解码
    jsondata = json.loads(jsondata) # 类型转换 string to dict
    content = jsondata.get('content')
    content = markdown.markdown(content)
    return {
        'md_content':content
        }

@post_bp.route('/upload/', methods=['POST'])
def upload():
    if not session.get('login'):
        return 'Permission denied'
    jsondata = request.get_data() # 此时格式为byte
    jsondata = jsondata.decode("utf-8") # 解码
    jsondata = json.loads(jsondata) # 类型转换 string to dict
    print(jsondata)
    title = jsondata['title']
    tags = jsondata['tags']
    date = jsondata['date']
    content = jsondata['content']
    id = jsondata['id']
    show = jsondata['show']
    show = 1 if show else 0
    if id == '':
        id = uuid.uuid4()
    with sql.connect(DB.sqlite) as conn:
        cur = conn.cursor()
        SQL = """INSERT OR REPLACE INTO post (
            id, title, tags, date, show
        ) VALUES(
            '{}', '{}', '{}', '{}', '{}'
        )
        """.format(id, title, tags, date, show)
        cur.execute(SQL)

        SQL_CONTENT = """INSERT OR REPLACE INTO content(id, content) VALUES(
            '{}', '{}'
        )""".format(id,content)
        cur.execute(SQL_CONTENT)

        SQL_IP = """INSERT OR REPLACE INTO ip(id) VALUES('{}')""".format(id)
        cur.execute(SQL_IP)

        conn.commit()

    return '上传成功'