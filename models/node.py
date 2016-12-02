from . import db
from . import ModelMixin


class Node(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    content = db.Column(db.String())
    keywords = db.Column(db.String())
    permit = db.Column(db.String())
    master = db.Column(db.String())
    parent_id = db.Column(db.Integer, default=0)
    topics = db.relationship('Topic', backref='board')

    def __init__(self, form):
        self.name = form.get('name', '')
        self.content = form.get("content", '')
        self.keywords = form.get("keywords", '板块')
        self.master = form.get('master', '')
        self.parent_id = form.get("parent_id", '')
        self.permit = form.get("permit", '')

    def _update(self, form):
        pass
