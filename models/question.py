from . import ModelMixin, utc
from . import db


class Question(db.Model, ModelMixin):
    __tablename__ = 'questions'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    solved = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    created_time = db.Column(db.Integer, default=utc())
    updated_time = db.Column(db.Integer, default=utc())
    deleted = db.Column(db.Integer, default=0)

    title = db.Column(db.String(255))
    expection = db.Column(db.Text())
    thinking = db.Column(db.Text())
    procedure = db.Column(db.Text())
    problems = db.Column(db.Text())
    code = db.Column(db.Text())
    # 外键
    user_id = db.Column(db.Integer, db.Foreign_key('users.id'))
    # 定义关系
    answers = db.relationship('Answer', backref='question')

    def __init__(self, form):
        self.title = form.get('title', '')
        self.expection = form.get('expection', '')
        self.thinking = form.get('thinking', '')
        self.procedure = form.get('procedure', '')
        self.problems = form.get('problems', '')
        self.code = form.get('code', '')

    def _update(self, form):
        for key in form:
            if key in self.__dict__:
                updated_value = form.get(key, '')
                if updated_value != '':
                    setattr(self, key, updated_value)
        self.updated_time = utc()
        self.save()
