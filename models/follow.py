from . import ModelMixin, utc
from . import db


class Follow(db.Model, ModelMixin):
    __tablename__ = 'follows'
    # 字段定义
    id = db.Column(db.Integer, primary_key=True)
    follow_id = db.Column(db.Integer)
    followed_id = db.Column(db.Integer)
    created_time = db.Column(db.Integer, default=utc())
    deleted = db.Column(db.Integer, default=0)

    @classmethod
    def delete(cls, follow_id, unfollow_id):
        follows = Follow.query.filter_by(follow_id=follow_id, unfollow_id=unfollow_id).all()
        for f in follows:
            f.deleted = 1
            f.save()

    def __init__(self, form):
        self.follow_id = int(form.get('follow_id', 0))
        self.followed_id = int(form.get('followed_id', 0))
