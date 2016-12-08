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
    return render_template('index.html', blogs=blog_list)


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    blog_form = BlogForm(user_id=current_user.id)
    if blog_form.validate_on_submit():
        form = request.form
        Blog.new(form)
        return redirect(url_for('.index'))
    return render_template('blog/add.html', form=blog_form)
