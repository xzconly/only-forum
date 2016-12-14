from routes import *
from flask_login import login_user, login_required
from forms import RegistrationForm, LoginForm, ProfileForm, PasswordForm

from models.follow import Follow

from utils import log

main = Blueprint('user', __name__)


@main.route('/register')
def register_view():
    register_form = RegistrationForm()
    return render_template('/user/register.html', form=register_form)


@main.route('/register', methods=['POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        form = request.form
        User.new(form)
        return redirect(url_for('.login'))
    else:
        flash('注册失败')
        return redirect(url_for('.register'))


@main.route('/login')
def login_view():
    login_form = LoginForm()
    return render_template('/user/login.html', form=login_form)


@main.route('/login', methods=['POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        form = request.form
        u = User(form)
        if u.validate_login():
            user = User.query.filter_by(username=u.username).first()
            login_user(user, login_form.remember_me.data)
            return redirect(url_for('blog.index'))
        else:
            flash('用户名或密码错误')


@main.route('/edit/<int:user_id>')
@login_required
def edit(user_id):
    profile_form = ProfileForm()
    user = User.query.get(user_id)
    return render_template('/user/edit_profile.html', user=user, form=profile_form)


@main.route('/edit/<int:user_id>', methods=['POST'])
@login_required
def update(user_id):
    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        form = request.form
        User.update(user_id, form)
        return redirect(url_for('.profile', user_id=user_id))
    else:
        flash('修改信息失败')
        return redirect(url_for('.edit', user_id=user_id))


@main.route('/edit_password')
@login_required
def edit_password():
    form = PasswordForm()
    user = current_user
    return render_template('/user/edit_password.html', user=user, form=form)


@main.route('/edit_password', methods=['POST'])
@login_required
def update_password():
    form = request.form
    status = current_user.update_password(form)
    if status:
        return redirect(url_for('.profile', user_id=current_user.id))
    else:
        flash('原密码填写错误')
        return redirect(url_for('.edit_password'))


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
