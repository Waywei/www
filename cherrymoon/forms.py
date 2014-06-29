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
            Length(min=2,max=8,message=u"长度为2到8个字符"),
            Regexp(ur'^[_a-zA-Z0-9\u4e00-\u9fa5]+$',message=u"输入的格式不正确")
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
    instagram  = URLField(u'instagram地址')

    weixin = TextField(u'微信')
    other1 = TextField(u'qq')

age = [(str(i),str(i)) for i in xrange(16,65)]
weight = [(str(i),str(i)+u"公斤(kg)") for i in xrange(40,150)]
height = [(str(i),str(i)+u"厘米(cm)") for i in xrange(150,230)]
 
class LookingForm(Form):
    find_active = SelectField(u'当前状态',choices=[
        ('1',u'活跃'),
        ('0',u'不活跃')
        ],validators=[DataRequired()])
    age = SelectField(u'年龄',choices= age,validators=[DataRequired()])
    height = SelectField(u'身高',choices=height,validators=[DataRequired()])
    weight = SelectField(u'体重',choices=weight,validators=[DataRequired()])
    #latitude = FloatField(u'坐标-x',validators=[DataRequired()])
    #longitude = FloatField(u'坐标-y',validators=[DataRequired()])
    like = SelectField(u'喜欢的体型',choices=[
        ('0',u'我不是很在意'),
        ('1',u"偏瘦"),
        ('2',u"正常"),
        ('3',u"偏胖"),
        ('4',u"很胖"),
        ('5',u"壮"),
        ],validators=[DataRequired()])
    info = TextAreaField(u'交友简介',validators=[DataRequired()])
    photo = TextField(u'照片',validators=[DataRequired()])

    question1 = TextAreaField(u'最喜欢做的三件事',validators=[DataRequired()])
    question2 = TextAreaField(u'最喜欢的三个音乐人，乐队',validators=[DataRequired()])
    question3 = TextAreaField(u'受到影响最多的三部电影',validators=[DataRequired()])
    question4 = TextAreaField(u'受到影响最多的三个人',validators=[DataRequired()])
    question5 = TextAreaField(u'未来必将发生的三件事',validators=[DataRequired()])
    question6 = TextAreaField(u'未来绝不会发生的三件事',validators=[DataRequired()])
class TopicForm(Form):
    title = TextField('title',validators=[DataRequired()])
    content  =  TextAreaField('content')
 
class CommentForm(Form):
    content  = TextAreaField('comment-content',
            validators=[Required(message=u'评论的内容不能为空')]
            )


class TreeHoleForm(Form):
    title = TextField('title',validators=[DataRequired()])
    content  =  TextAreaField('content')
 
class TreeCommentForm(Form):
    content  = TextAreaField('comment-content',
            validators=[Required(message=u'评论的内容不能为空')]
            )



class ForgetForm(Form):
    username = TextField(u'用户名',validators=[DataRequired()])
    email    = EmailField(u'邮箱账号',validators=[DataRequired()])

class ResetPasswordForm(Form):
    password = PasswordField(u'密码',validators=[DataRequired()])
    confirm = PasswordField(u'再次输入',validators=[DataRequired()])

    def validate_confirm(self, field):
        if field.data != self.password.data:
            raise ValueError(u"两次输入的密码不一致")

imglist = ('jpg','png','jpeg')
class UploadForm(Form):
    uploads = FileField(u'选择图像文件',
        validators = [
                FileRequired(),
                FileAllowed(imglist,u'图片只支持jpg png jpeg格式')
            ]
        )
