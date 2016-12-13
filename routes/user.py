from routes import *
from flask_login import login_user, login_required
from forms import RegistrationForm, LoginForm

from models.follow import Follow

from utils import log


main = Blueprint('user', __name__)


@main.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        form = request.form
        user = User(form)
        user.password = User.salted_password(user.password)
        user.save()
        return redirect(url_for('.login'))
    return render_template('/user/register.html', form=register_form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        form = request.form
        u = User(form)
        if u.validate_login():
            user = User.query.filter_by(username=u.username).first()
            login_user(user, login_form.remember_me.data)
            return redirect(url_for('index.index'))
        else:
            flash('用户名或密码错误')
    return render_template('/user/login.html', form=login_form)


@main.route('/edit/<int:model_id>')
@login_required
def edit(model_id):
    user = User.query.get(model_id)
    return render_template('/user/edit_profile.html', user=user)


@main.route('/update/<int:model_id>', methods=['POST'])
@login_required
def update(model_id):
    form = request.form
    User.update(model_id, form)
    return redirect(url_for('.profile', model_id=model_id))


@main.route('/edit_password/<int:model_id>')
@login_required
def edit_password(model_id):
    user = User.query.get(model_id)
    return render_template('/user/edit_password.html', user=user)


@main.route('/update_password/<int:model_id>', methods=['POST'])
@login_required
def update_password(model_id):
    form = request.form
    user = User.query.get(model_id)
    result = user.update_password(form)
    if result is not None:
        return result
    return redirect(url_for('.profile'))


@main.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    follow_status = current_user.get_follow_status(user_id)
    return render_template('/user/profile.html', user=user, status=follow_status)


@main.route('/upload', methods=['POST'])
def upload_file():
    import json
    import config
    # 通过 request.files 访问上传的文件
    # uploaded 是上传时候的文件名
    f = request.files.get('uploaded')
    if f:
        user_id = get_user_id()
        file_name = str(user_id)
        filename = file_name + '.' + f.filename.split('.')[-1]
        path = config.uploads_avatar_dir + filename
        f.save(path)
        msg_dict = dict(
            msg='头像上传成功',
            status=1,
            filename=filename,
            img_url=url_for('.uploaded_file', filename=filename),
        )
    else:
        msg_dict = dict(
            msg='头像上传失败',
            status=0,
        )
    return json.dumps(msg_dict)


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    # 用这个函数直接返回文件的响应
    import config
    return flask.send_from_directory(config.uploads_avatar_dir, filename)


@main.route('/follow')
@login_required
def follow():
    followed = Follow.query.filter_by(follow_id=current_user.id).all()
    users = User.get_followed(followed)
    return render_template('/user/follow.html', users=users)


@main.route('/followed')
@login_required
def followed():
    follow = Follow.query.filter_by(followed_id=current_user.id).all()
    users = User.get_follow(follow)
    return render_template('/user/followed.html', users=users)
