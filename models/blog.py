from . import ModelMixin, utc
from . import db


class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    # 字段定义
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    thumb = db.Column(db.String(255))
    views = db.Column(db.Integer, default=0)
    upvotes = db.Column(db.Integer, default=0)
    tag = db.Column(db.String(100))
    created_time = db.Column(db.Integer, default=utc())
    updated_time = db.Column(db.Integer, default=utc())
    deleted = db.Column(db.Integer, default=0)
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 定义关系
    comments = db.relationship('Comment', backref='blog')

    @classmethod
    def new(cls, form):
        blog = cls(form)
        # 抓取/设置 默认缩略图
        blog.set_thumb()
        blog.save()

    @classmethod
    def upvote(cls, blog_id):
        blog = cls.query.get(blog_id)
        blog.upvotes += 1
        blog.save()

    @classmethod
    def add_views(cls, blog_id):
        blog = cls.query.get(blog_id)
        blog.views += 1
        blog.save()

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.tag = form.get('tag', '')
        self.user_id = int(form.get('user_id', 0))

    def _update(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.tag = form.get('tag', '')
        self.updated_time = utc()
        self.save()

    def set_thumb(self):
        self.thumb = Blog.random_thumb()
        # Todo  从 content 中抓取第一张图片作为 缩略图 （如果有）

    def is_owner(self, user_id):
        return self.user_id == user_id

    @staticmethod
    def random_thumb():
        import random
        thumb = random.randint(1, 10)
        return str(thumb) + '.jpg'
