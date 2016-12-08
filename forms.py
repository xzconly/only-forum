from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, \
    SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

from models.user import User


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 16, message='用户名长度必须在6~16中间')])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 16, message='密码长度必须在6~16中间'),
                                               EqualTo('password2', message='两次输入密码不一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册')


class LoginForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')


class BlogForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('标题不能为空')])
    tag = StringField('标签')
    content = TextAreaField('正文', validators=[DataRequired('内容不能为空')])
    user_id = HiddenField('user_id')
    submit = SubmitField('发表博客')
