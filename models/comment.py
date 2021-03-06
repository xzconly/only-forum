from . import ModelMixin, utc
from . import db


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    created_time = db.Column(db.Integer, default=utc())
    updated_time = db.Column(db.Integer, default=utc())
    deleted = db.Column(db.Integer, default=0)
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    # 定义关系
    reply_comments = db.relationship('ReplyComment', backref='comment')

    def __init__(self, form):
        self.content = form.get('content', '')
        self.blog_id = int(form.get('blog_id', 0))
        self.user_id = int(form.get('user_id', 0))

    def _update(self, form):
        self.content = form.get('content', '')
        self.updated_time = utc()
        self.save()
