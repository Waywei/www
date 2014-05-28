# -*- coding: utf-8 -*-  
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField,SelectField, SubmitField 
from wtforms import FloatField, IntegerField
from wtforms.validators import Required, ValidationError,DataRequired, Regexp, Length, Email
from flask_wtf.html5 import EmailField, URLField
from flask_wtf.file import FileField,FileAllowed,FileRequired
from werkzeug import secure_filename
import os
from cherrymoon.models import User
import re


class SignupForm(Form):
    email = EmailField(u'登陆邮箱',validators=[
            Required(message=u'登陆邮箱不能为空'),
            Email()
        ])
    username = TextField(u'用户名',validators=[
            Required(message=u'用户名不能为空'),
            Length(min=2,max=16),
            Regexp(ur'^[\u4e00-\u9fa5_a-zA-Z0-9]+$',message=u"用户名只能是字母中文数字跟下划线")
        ])
    password = PasswordField(u'登陆密码', validators=[
            Required(message=u'密码不能为空')
        ])

    def validate_username(self,field):
        data = field.data.lower()
        if User.query.filter_by(username=data).count():
            raise ValidationError(u'这个用户名已被注册')

    def validate_email(self,field):
        data = field.data.lower()
        if User.query.filter_by(email = data).count():
            raise ValidationError(u'这个邮箱地址已经注册过了')

class SigninForm(Form):
    email = EmailField(u'邮箱账号',validators=[
            Required(message=u'登陆邮箱不能为空'),
            Email()
        ])
    password = PasswordField(u'登录密码',validators=[
            Required(message=u'登陆密码不能为空')
        ])

    def validate_password(self,field):
        email = self.email.data
        pwd = field.data
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValidationError(u'邮箱或者密码有错误')
        if user.check_password(pwd):
            self.user = user
            return user
        raise ValidationError(u'邮箱或者密码有错误') 

class SettingForm(Form):
    website = URLField(u'个人网站')
    city = TextField(u'所在城市')
    weibo = URLField(u'微博地址')
    instagram  = URLField(u'instagram地址')
    flickr = URLField(u'flickr地址')
    twitter = URLField(u'twitter地址')
    renren = URLField(u'人人地址')
    facebook = URLField(u'facebook地址')
    description = TextAreaField(u'个人介绍')

class FindingForm(Form):
    is_active = SelectField(u'当前状态',choices=[
        ('1',u'活跃'),
        ('0',u'不活跃')
        ],validators=[DataRequired()])
    age = IntegerField(u'年龄',validators=[DataRequired()])
    height = IntegerField(u'身高',validators=[DataRequired()])
    weight = IntegerField(u'体重',validators=[DataRequired()])
    latitude = FloatField(u'坐标-x',validators=[DataRequired()])
    longitude = FloatField(u'坐标-y',validators=[DataRequired()])
    like = SelectField(u'喜欢的类型',choices=[
        ('0',u'全部'),
        ('1',u"偏瘦"),
        ('2',u"偏胖"),
        ('3',u"很重"),
        ],validators=[DataRequired()])
    findinfo = TextAreaField(u'交友简介',validators=[DataRequired()])

class TopicForm(Form):
    title = TextField('title',validators=[DataRequired()])
    content  =  TextAreaField('content')
 
class CommentForm(Form):
    content  = TextAreaField('comment-content',
            validators=[Required(message=u'评论的内容不能为空')]
            )

imglist = ('jpg','png','jpeg')
class UploadForm(Form):
    uploads = FileField(u'选择图像文件',
        validators = [
                FileRequired(),
                FileAllowed(imglist,u'图片只支持jpg png jpeg格式')
            ]
        )
