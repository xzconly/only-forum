from models.topic import Topic
from models.comment import Comment
from models.node import Node
from routes import *

from utils import log


main = Blueprint('topic', __name__)

Model = Topic


def require_login():
    u = current_user()
    if u is None:
        return redirect(url_for('user.login'))



# 一次性给蓝图中的每个路由加上管理权限验证
# 这样就不用手动去给每个函数分别加这个验证了
# (login_required 的方式就是手动一个个加)
main.before_request(require_login)


@main.route('/')
def index():
    model_list = Model.query.all()
    return render_template('/topic/index.html', topics=model_list)


@main.route('/add')
def new():
    u = current_user()
    nodes = Node.query.filter_by(deleted=0).all()
    return render_template('/topic/add.html', user_id=u.id, board=nodes)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model.new(form)
    user = m.user
    user.credit += 10
    user.save()
    return redirect(url_for('.index'))


@main.route('/topic/<int:model_id>')
def detail(model_id):
    u = current_user()
    model = Model.query.get(model_id)
    return render_template('/topic/detail.html', topic=model, user_id=u.id)


@main.route('/add_comment', methods=['POST'])
def add_comment():
    form = request.form
    topic_id = int(form.get('topic_id', ''))
    Comment.new(form)
    return redirect(url_for('.detail', model_id=topic_id))
