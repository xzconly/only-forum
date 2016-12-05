import flask
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for

from functools import wraps

from models.user import User


# 通过 session 来获取当前登录的用户
def current_user():
    user_id = session.get('user_id', '')
    u = User.query.get(user_id)
    return u


# 这个参数 f 实际上就是路由函数
def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            # 用户未登录, 重定向到登录页面
            return redirect(url_for('user.login'))
        else:
            # 用户已经登录, 扔给路由函数处理
            return f(*args, **kwargs)
    return function


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u is None or not u.is_admin():
            # 用户非管理员
            return redirect(url_for('topic.index'))
        else:
            # 用户是管理员, 扔给路由函数处理
            return f(*args, **kwargs)
    return function


# 用于 路由添加统一验证
def require_login():
    u = current_user()
    if u is None:
        return redirect(url_for('user.login'))


# 这是一个要求管理员权限的函数
def require_admin():
    u = current_user()
    # u 不存在或者不是管理员
    if u is None or not u.is_admin():
        flask.abort(404)
