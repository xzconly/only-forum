from models.blog import Blog
from models.comment import Comment
from models.vote import Vote
from routes import *

from forms import BlogForm, BlogCommentForm

from utils import log


main = Blueprint('blog', __name__)


@main.route('/')
def index():
    blog_list = Blog.query.filter_by(deleted=0).all()
    return render_template('/blog/index.html', blogs=blog_list)


@main.route('/my_blogs')
@login_required
def user_blog():
    blog_list = Blog.query.filter_by(user_id=current_user.id, deleted=0).all()
    return render_template('/blog/user_index.html', blogs=blog_list)


@main.route('/<int:blog_id>')
def detail(blog_id):
    blog_comment_form = BlogCommentForm(user_id=current_user.id, blog_id=blog_id, topic_id=-1)
    blog = Blog.query.get(blog_id)
    comments = Comment.query.filter_by(blog_id=blog_id).all()
    Blog.add_views(blog_id)
    return render_template('/blog/detail.html', blog=blog, comments=comments, form=blog_comment_form)


@main.route('/<int:blog_id>', methods=['POST'])
@login_required
def add_comment(blog_id):
    blog_comment_form = BlogCommentForm(user_id=current_user.id, blog_id=blog_id, topic_id=-1)
    if blog_comment_form.validate_on_submit():
        form = request.form
        Comment.new(form)
        return redirect(url_for('.detail', blog_id=blog_id))


@main.route('/add')
@login_required
def new():
    blog_form = BlogForm(user_id=current_user.id)
    return render_template('/blog/add.html', form=blog_form)


@main.route('/add', methods=['POST'])
@login_required
def add():
    blog_form = BlogForm(user_id=current_user.id)
    if blog_form.validate_on_submit():
        form = request.form
        Blog.new(form)
        return redirect(url_for('.index'))


@main.route('/edit/<int:blog_id>')
@login_required
def edit(blog_id):
    blog = Blog.query.get(blog_id)
    blog_auth(blog)
    blog_form = BlogForm(user_id=current_user.id)
    blog_form.content.data = blog.content
    return render_template('/blog/edit.html', form=blog_form, blog=blog)


@main.route('/edit/<int:blog_id>', methods=['POST'])
@login_required
def update(blog_id):
    blog_form = BlogForm(user_id=current_user.id)
    if blog_form.validate_on_submit():
        form = request.form
        Blog.update(blog_id, form)
        return redirect(url_for('.detail', blog_id=blog_id))


@main.route('/delete/<int:blog_id>')
@login_required
def delete(blog_id):
    blog = Blog.query.get(blog_id)
    blog_auth(blog)
    Blog.delete(blog_id)
    return redirect(url_for('.index'))


@main.route('/upvote', methods=['POST'])
@login_required
def upvote():
    import json
    form = request.form
    vote = Vote(form)
    if not vote.is_voted():
        vote.save()
        blog_id = int(form.get('blog_id', 0))
        Blog.upvote(blog_id)
        blog = Blog.query.get(blog_id)
        upvotes = blog.upvotes
        response = dict(
            status=1,
            vote_num=upvotes,
            msg='点赞成功'
        )
    else:
        response = dict(
            status=0,
            msg='点赞失败'
        )
    return json.dumps(response)


@main.route('/thumb/<filename>')
def thumb_img(filename):
    import config
    return flask.send_from_directory(config.uploads_thumb_dir, filename)
