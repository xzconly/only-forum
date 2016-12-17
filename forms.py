from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, \
    SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError

from models.user import User

from utils import log


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 16, message='用户名长度必须在6~16中间')],
                           render_kw={'placeholder': '用户名长度在6~16之间'})
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入有效的邮箱地址')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 16, message='密码长度必须在6~16中间'),
                                               EqualTo('password2', message='两次输入密码不一致')],
                                               render_kw = {'placeholder': '密码长度在6~16之间'})
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        email = User.query.filter_by(email=field.data).first()
        if email:
            raise ValidationError('该邮箱已注册')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user is None:
            raise ValidationError('用户名不存在')


class ProfileForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入有效的邮箱地址')])
    avatar = StringField('头像')
    qq = StringField('qq', validators=[Length(0, 20, message='qq长度不超过20')])
    signature = StringField('签名')
    submit = SubmitField('修改')


class PasswordForm(FlaskForm):
    origin_pwd = PasswordField('原密码', validators=[DataRequired()])
    new_pwd = PasswordField('新密码', validators=[DataRequired(), Length(6, 16, message='密码长度必须在6~16中间'),
                                               EqualTo('confirm_pwd', message='两次输入密码不一致')])
    confirm_pwd = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('修改')


class BlogForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('标题不能为空')])
    tag = StringField('标签')
    content = TextAreaField('正文', validators=[DataRequired('内容不能为空')])
    user_id = HiddenField('user_id')
    submit = SubmitField('发表博客')


class BlogCommentForm(FlaskForm):
    content = TextAreaField('评论', validators=[DataRequired('评论不能为空')])
    user_id = HiddenField('user_id')
    blog_id = HiddenField('blog_id')
    submit = SubmitField('发表评论')


class ReplyCommentForm(FlaskForm):
    content = TextAreaField('', validators=[DataRequired('回复内容不能为空')])
    submit = SubmitField('提交')

