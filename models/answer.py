from . import ModelMixin, utc
from . import db

from models.question import Question


class Answer(db.Model, ModelMixin):
    __tablename__ = 'answers'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    created_time = db.Column(db.Integer, default=utc())
    updated_time = db.Column(db.Integer, default=utc())
    deleted = db.Column(db.Integer, default=0)
    # 定义外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.question_id = form.get('question_id', '')
        question = Question.query.get(self.question_id)
        question.updated_time = utc()

    def _update(self, form):
        self.content = form.get('content', '')
        self.updated_time = utc()
        self.question.updated_time = utc()
        self.save()
