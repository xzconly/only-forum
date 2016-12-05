from models.node import Node
from models.topic import Topic
from routes import *

from utils import log


main = Blueprint('node', __name__)

Model = Node


# 一次性给蓝图中的每个路由加上管理权限验证
# 这样就不用手动去给每个函数分别加这个验证了
# (login_required 的方式就是手动一个个加)
main.before_request(require_login)


@main.route('/')
def index():
    model_list = Model.query.filter_by(deleted=0).all()
    return render_template('/node/index.html', nodes=model_list)


@main.route('/add')
@admin_required
def new():
    return render_template('/node/add.html')


@main.route('/add', methods=['POST'])
@admin_required
def add():
    form = request.form
    m = Model.new(form)
    return redirect(url_for('.index'))


@main.route('/<int:model_id>')
def detail(model_id):
    model = Model.query.get(model_id)
    return render_template('/node/detail.html', node=model)


@main.route('/edit/<int:model_id>')
@admin_required
def edit_view(model_id):
    model = Model.query.get(model_id)
    return render_template('/node/edit.html', node=model)


@main.route('/update', methods=['POST'])
@admin_required
def update():
    form = request.form
    model_id = int(form.get('model_id'))
    Model.update(model_id, form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:model_id>')
@admin_required
def delete(model_id):
    Model.delete(model_id)
    return redirect(url_for('.index'))
