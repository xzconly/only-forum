from . import ModelMixin, utc
from . import db


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    views = db.Column(db.Integer, default=0)
    created_time = db.Column(db.Integer, default=utc())
    updated_time = db.Column(db.Integer, default=utc())
    deleted = db.Column(db.Integer, default=0)
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    # 定义关系
    comments = db.relationship('Comment', backref='topic')

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.board_id = form.get('board_id', 0)

    def _update(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.updated_time = utc()
        self.save()
