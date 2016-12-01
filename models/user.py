from . import ModelMixin, utc
from . import db


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))
    email = db.Column(db.String(30))
    qq = db.Column(db.String(20))
    signature = db.Column(db.String(255))
    credit = db.Column(db.Integer, default=0)
    created_time = db.Column(db.Integer)

    # 定义关系
    topics = db.relationship('Topic', backref='user')
    comments = db.relationship('Comment', backref='user')
    questions = db.relationship('Question', backref='user')
    answers = db.relationship('Answer', backref='user')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')
        self.qq = form.get('qq', '')
        self.signature = form.get('signature', '')
        self.created_time = utc()

    def sha1ed_password(self, pwd):
        """
        sha1 加密密码
        """
        import hashlib
        s = hashlib.sha1(pwd.encode('ascii'))
        return s.hexdigest()

    def salted_password(self, pwd):
        """
        对 sha1 加密后的密码， 加盐
        """
        salt = 'a32qfs342w2fsf23q323f'
        sha1_pwd = self.sha1ed_password(pwd)
        salt_pwd = self.sha1ed_password(sha1_pwd + salt)
        return salt_pwd

    def valid_username(self):
        return User.query.filter_by(username=self.username).first() is None

    def valid(self):
        """
        验证 注册用户的 合法性
        """
        valid_username = self.valid_username()
        valid_username_len = len(self.username) >= 6
        valid_password_len = len(self.password) >= 6
        msgs = []
        if not valid_username:
            message = '用户名已存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度不小于 6'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度不小于 6'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs

    def validate_login(self):
        msgs = []
        valid_username = True
        valid_password = True
        user = User.query.filter_by(username=self.username).first()
        self.password = self.salted_password(self.password)
        if user is None:
            valid_username = False
            message = '用户名不存在'
            msgs.append(message)
        elif user.password != self.password:
            valid_password = False
            message = '密码错误'
            msgs.append(message)
        status = valid_username and valid_password
        return status, msgs

    def validate_auth(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        username_equals = username == self.username
        password_equals = password == self.password
        return username_equals and password_equals

    def _update(self, form):
        """
        修改密码
        """
        if self.validate_auth(form):
            self.password = form.get('new_password', self.password)
            self.save()
        else:
            return '请输入正确的用户名和密码'
