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
    def handle_follow(cls, follow_ids):
        follow_id = follow_ids.get('follow_id', '')
        followed_id = follow_ids.get('followed_id', '')
        if follow_id == '' or followed_id == '':
            return 0
        follow_id = int(follow_id)
        followed_id = int(followed_id)
        follow = Follow.query.filter_by(follow_id=follow_id, followed_id=followed_id).first()
        # 没有关注过
        if follow is None:
            form = dict(
                follow_id=follow_id,
                followed_id=followed_id,
            )
            Follow.new(form)
            return 1
        elif follow is not None:
            # 取消关注后 重新关注
            if follow.deleted == 1:
                follow.deleted = 0
                follow.save()
                return 1
            else:
                # 取消关注
                follow.deleted = 1
                follow.save()
                return 2

    def __init__(self, form):
        self.follow_id = int(form.get('follow_id', 0))
        self.followed_id = int(form.get('followed_id', 0))
