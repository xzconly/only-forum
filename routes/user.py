from models.user import User
from routes import *

from utils import log


main = Blueprint('user', __name__)

Model = User


@main.route('/register')
def register_view():
    return render_template('user/register.html')


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    user = Model(form)
    status, msgs = user.valid()
    if status:
        user.save()
        return redirect(url_for('.login'))
    else:
        return redirect(url_for('.register'))


@main.route('/login')
def login_view():
    return render_template('user/login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = Model(form)
    status, msgs = u.validate_login()
    if status:
        user = Model.query.filter_by(username=u.username).first()
        # 设置 session 返回响应 Set-Cookie
        # 浏览器生成 cookie
        session['user_id'] = user.id
        return redirect(url_for('index.index'))
    else:
        return redirect(url_for('.login'))


@main.route('/edit/<int:model_id>')
@login_required
def edit(model_id):
    user = Model.query.get(model_id)
    return render_template('/user/edit_profile.html', user=user)

@main.route('/update/<int:model_id>', methods=['POST'])
@login_required
def update(model_id):
    form = request.form
    Model.update(model_id, form)
    return redirect(url_for('.profile', model_id=model_id))


@main.route('/edit_password/<int:model_id>')
@login_required
def edit_password(model_id):
    user = Model.query.get(model_id)
    return render_template('/user/edit_password.html', user=user)


@main.route('/update_password/<int:model_id>', methods=['POST'])
@login_required
def update_password(model_id):
    form = request.form
    user = Model.query.get(model_id)
    result = user._update_password(form)
    if result is not None:
        return result
    return redirect(url_for('.profile', model_id=model_id))


@main.route('/profile/<int:model_id>')
@login_required
def profile(model_id):
    user = Model.query.get(model_id)
    return render_template('/user/profile.html', user=user)
