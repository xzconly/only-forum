from . import ModelMixin, utc
from . import db
from flask_login import UserMixin

from models.follow import Follow

from utils import log


class User(db.Model, ModelMixin, UserMixin):
    __tablename__ = 'users'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))
    email = db.Column(db.String(30))
    nickname = db.Column(db.String(30))
    avatar = db.Column(db.String(255))
    qq = db.Column(db.String(20))
    signature = db.Column(db.String(255))
    credit = db.Column(db.Integer, default=0)
    role = db.Column(db.Integer, default=10)
    created_time = db.Column(db.Integer, default=utc())
    updated_time = db.Column(db.Integer, default=utc())

    # 定义关系
    topics = db.relationship('Topic', backref='user')
    comments = db.relationship('Comment', backref='user')
    questions = db.relationship('Question', backref='user')
    answers = db.relationship('Answer', backref='user')
    blogs = db.relationship('Blog', backref='user')
    reply_comments = db.relationship('ReplyComment', backref='user')

    @classmethod
    def new(cls, form):
        user = cls(form)
        user.password = cls.salted_password(user.password)
        user.save()

    @classmethod
    def sha1ed_password(cls, pwd):
        """
        sha1 加密密码
        """
        import hashlib
        s = hashlib.sha1(pwd.encode('ascii'))
        return s.hexdigest()

    @classmethod
    def salted_password(cls, pwd):
        """
        对 sha1 加密后的密码， 加盐
        """
        import config
        salt = config.salt
        sha1_pwd = cls.sha1ed_password(pwd)
        salt_pwd = cls.sha1ed_password(sha1_pwd + salt)
        return salt_pwd

    @classmethod
    def get_followed(cls, followed):
        users = []
        for f in followed:
            user = User.query.get(f.followed_id)
            users.append(user)
        return users

    @classmethod
    def get_follow(cls, follow):
        users = []
        for f in follow:
            user = User.query.get(f.follow_id)
            users.append(user)
        return users

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')
        self.nickname = form.get('nickname', '')
        self.avatar = form.get('avatar', 'default.png')
        self.qq = form.get('qq', '')
        self.signature = form.get('signature', '')

    def _update(self, form):
        for key in form:
            if key in self.__dict__:
                updated_value = form.get(key, '')
                if updated_value != '':
                    setattr(self, key, updated_value)
        self.updated_time = utc()
        self.save()

    def is_admin(self):
        return self.role == 1

    def validate_login(self):
        user = User.query.filter_by(username=self.username).first()
        pwd = self.salted_password(self.password)
        return user is not None and pwd == user.password

    def get_avatar_thumb(self, img_size):
        from PIL import Image
        import os
        import config
        img = os.path.abspath(config.uploads_avatar_dir + self.avatar)
        size = img_size, img_size
        file, ext = os.path.splitext(self.avatar)
        thumb_img_name = file + '_thumb' + ext
        thumb_path = config.uploads_avatar_dir + thumb_img_name
        if not os.path.exists(thumb_path):
            im = Image.open(img)
            im.thumbnail(size)
            im.save(thumb_path)
        return thumb_img_name

    def get_follow_status(self, user_id):
        """
        是否已关注 user_id 用户
        """
        if self.id == user_id:
            status = 0
        else:
            follow = Follow.query.filter_by(follow_id=self.id, followed_id=user_id).first()
            if follow is not None and follow.deleted == 0:
                status = 1
            else:
                status = 2
        return status

    def validate_auth(self, password):
        password = self.salted_password(password)
        return password == self.password

    def update_password(self, form):
        """
        修改密码
        """
        origin_pwd = form.get('origin_pwd')
        new_pwd = form.get('new_pwd')
        status = self.validate_auth(origin_pwd)
        if status:
            self.password = self.salted_password(new_pwd)
            self.save()
        return status
