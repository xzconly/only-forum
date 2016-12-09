from . import ModelMixin, utc
from . import db
from flask_login import UserMixin

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

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')
        self.nickname = form.get('nickname', '')
        self.avatar = form.get('avatar', 'default.png')
        self.qq = form.get('qq', '')
        self.signature = form.get('signature', '')

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

    def validate_auth(self, form):
        msgs = []
        username = form.get('username', '')
        password = form.get('password', '')
        password = self.salted_password(password)
        username_equals = username == self.username
        password_equals = password == self.password
        status = username_equals and password_equals
        if not status:
            message = '用户名或密码错误'
            msgs.append(message)
        return status, msgs

    def valid_password(self, form):
        """
        验证修改的 新密码
        """
        msgs = []
        new_password = form.get('new_password', '')
        confirm_password = form.get('confirm_password', '')
        valid_password_len = len(new_password) >= 6
        valid_confirm_password = new_password == confirm_password
        if not valid_password_len:
            message = '新密码长度不小于 6'
            msgs.append(message)
        elif not valid_confirm_password:
            message = '两次输入的密码不一致'
            msgs.append(message)
        status = valid_password_len and valid_confirm_password
        return status, msgs

    def update_password(self, form):
        """
        修改密码
        """
        auth_status, auth_msgs = self.validate_auth(form)
        confirm_status, confirm_msgs = self.valid_password(form)
        if auth_status:
            if confirm_status:
                self.password = form.get('new_password', self.password)
                self.password = self.salted_password(self.password)
                self.save()
            else:
                return ','.join(confirm_msgs)
        else:
            return ','.join(auth_msgs)

    def _update(self, form):
        for key in form:
            if key in self.__dict__:
                updated_value = form.get(key, '')
                if updated_value != '':
                    setattr(self, key, updated_value)
        self.updated_time = utc()
        self.save()
