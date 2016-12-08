from models.blog import Blog
from models.comment import Comment
from routes import *
from flask_login import login_required, current_user

from forms import BlogForm

from utils import log


main = Blueprint('blog', __name__)


@main.route('/')
def index():
    blog_list = Blog.query.filter_by(deleted=0).all()
    return render_template('/blog/index.html', blogs=blog_list)


@main.route('/<int:blog_id>')
def detail(blog_id):
    blog = Blog.query.get(blog_id)
    return render_template('detail.html', blog=blog)


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    log('current_user', current_user)
    blog_form = BlogForm(user_id=current_user.id)
    if blog_form.validate_on_submit():
        form = request.form
        blog = Blog(form)
        # 抓取/设置 默认缩略图
        blog.set_thumb()
        blog.save()
        return redirect(url_for('.index'))
    return render_template('blog/add.html', form=blog_form)


@main.route('/thumb/<filename>')
def thumb_img(filename):
    import config
    return flask.send_from_directory(config.uploads_thumb_dir, filename)
