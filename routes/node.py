from models.node import Node
from models.topic import Topic
from routes import *

from utils import log


main = Blueprint('node', __name__)

Model = Node


def require_login():
    u = current_user()
    if u is None:
        return redirect(url_for('user.login'))


# 这是一个要求管理员权限的函数
def admin_required():
    u = current_user()
    # u 不存在或者不是管理员
    if u is None or not u.is_admin():
        flask.abort(404)


# 一次性给蓝图中的每个路由加上管理权限验证
# 这样就不用手动去给每个函数分别加这个验证了
# (login_required 的方式就是手动一个个加)
main.before_request(require_login)
main.before_request(admin_required)


@main.route('/')
def index():
    model_list = Model.query.filter_by(deleted=0).all()
    return render_template('/node/index.html', nodes=model_list)


@main.route('/add')
def new():
    return render_template('/node/add.html')


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model.new(form)
    return redirect(url_for('.index'))


@main.route('/node/<int:model_id>')
def detail(model_id):
    model = Model.query.get(model_id)
    return render_template('/node/detail.html', node=model)


@main.route('/edit/<int:model_id>')
def edit_view(model_id):
    model = Model.query.get(model_id)
    return render_template('/node/edit.html', node=model)


@main.route('/update', methods=['POST'])
def update():
    form = request.form
    model_id = int(form.get('model_id'))
    Model.update(model_id, form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:model_id>')
def delete(model_id):
    Model.delete(model_id)
    return redirect(url_for('.index'))
