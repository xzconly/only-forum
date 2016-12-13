from . import ModelMixin, utc
from . import db


class ReplyComment(db.Model, ModelMixin):
    __tablename__ = 'reply_comments'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    reply_id = db.Column(db.Integer)
    reply_user_id = db.Column(db.Integer)
    reply_username = db.Column(db.String(30))
    created_time = db.Column(db.Integer, default=utc())
    deleted = db.Column(db.Integer, default=0)
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.reply_id = int(form.get('reply_id', 0))
        self.reply_user_id = int(form.get('reply_user_id', 0))
        self.reply_username = form.get('reply_username', '')
        self.user_id = int(form.get('user_id', 0))
        self.comment_id = int(form.get('comment_id', 0))
