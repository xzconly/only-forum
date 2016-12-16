from . import db
from . import ModelMixin


class Node(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    content = db.Column(db.Text)
    keywords = db.Column(db.String(100))
    permit = db.Column(db.Integer, default=0)
    master = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Integer, default=0)
    # 定义关系
    topics = db.relationship('Topic', backref='board')

    def __init__(self, form):
        self.name = form.get('name', '')
        self.content = form.get("content", '')
        self.keywords = form.get("keywords", '版块')
        self.master = form.get('master', 0)
        self.parent_id = int(form.get("parent_id", 0))
        self.permit = form.get("permit", 0)

    def _update(self, form):
        for key in form:
            if key in self.__dict__:
                updated_value = form.get(key, '')
                if updated_value != '':
                    setattr(self, key, updated_value)
        self.save()
