from models.question import Question
from models.answer import Answer
from routes import *

from utils import log


main = Blueprint('question', __name__)

Model = Question


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
    model_list = Model.query.filter_by(deleted=0).all()
    return render_template('/question/index.html', questions=model_list)


@main.route('/add')
def new():
    u = current_user()
    return render_template('/question/add.html', user_id=u.id)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model.new(form)
    return redirect(url_for('.index'))


@main.route('/detail/<int:model_id>')
def detail(model_id):
    u = current_user()
    model = Model.query.get(model_id)
    return render_template('/question/detail.html', question=model, user_id=u.id)


@main.route('/add_answer', methods=['POST'])
def add_answer():
    form = request.form
    question_id = int(form.get('question_id', ''))
    Answer.new(form)
    return redirect(url_for('.detail', model_id=question_id))
