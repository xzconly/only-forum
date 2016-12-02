from models.user import User
from routes import *


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
        return msgs


@main.route('/login')
def login_view():
    return render_template('user/login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    user = Model(form)
    status, msgs = user.validate_login()
    if status:
        return redirect(url_for('index.index'))
    else:
        return msgs


@main.route('/update/<int:model_id>', methods=['POST'])
def update(model_id):
    form = request.form
    Model.update(model_id, form)
    return redirect(url_for('.profile'))


@main.route('/update_password/<int:model_id>', methods=['POST'])
def update_password(model_id):
    form = request.form
    m = Model.query.get(model_id)
    m._update_password(form)
    return redirect(url_for('.profile'))


@main.route('/profile/<int:model_id>')
def profile(model_id):
    user = Model.query.get(model_id)
    return render_template('/user/profile.html', user=user)
