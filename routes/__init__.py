import flask
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import flash
from flask import send_from_directory
from flask import session
from flask import url_for
from flask_login import login_required, current_user
from sqlalchemy import desc

from functools import wraps

from models.user import User


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
    if current_user.id == '':
        flash('请先登录')
        return redirect(url_for('user.login'))


# 博客 修改/删除 权限验证
def blog_auth(blog):
    if not blog.is_owner(current_user.id):
        flash('您没有权限进行此操作')
        flask.abort(404)


# 这是一个要求管理员权限的函数
def require_admin():
    u = current_user()
    # u 不存在或者不是管理员
    if u is None or not u.is_admin():
        flask.abort(404)


def get_user_id():
    """
    获取 user_id
    如果当前未登录，返回 最新用户的 id + 1 值
    """
    user = current_user()
    if user is not None:
        return user.id
    else:
        last_user = User.query.order_by(desc(User.id)).first()
        return last_user.id + 1
