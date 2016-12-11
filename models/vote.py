from . import ModelMixin, utc
from . import db

from utils import log


class Vote(db.Model, ModelMixin):
    __tablename__ = 'votes'
    # 字段定义
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    blog_id = db.Column(db.Integer)
    created_time = db.Column(db.Integer, default=utc())

    def __init__(self, form):
        self.user_id = int(form.get('user_id', 0))
        self.blog_id = int(form.get('blog_id', 0))

    def is_voted(self):
        vote = Vote.query.filter_by(user_id=self.user_id).first()
        return vote is not None and vote.blog_id == self.blog_id
