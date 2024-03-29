# -*- coding: utf-8 -*-  
from cherrymoon.ext.db import db
from werkzeug import security
 
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime
from sqlalchemy import Float
from datetime import datetime


class User(db.Model):
    id          = Column(Integer, primary_key = True)
    username    = Column(String(40),nullable  = False,index = True, unique = True)
    email       = Column(String(120),nullable = False,index = True, unique = True)
    password    = Column(String(120),nullable= False)
    token       = Column(String(20))
    
    avatar      = Column(String(40),default='')
    is_active   = Column(Boolean,default='1')
    
    hp          = Column(Integer,default="200")

    description = Column(String(500),default='')
    city        = Column(String(40),default='')
    website     = Column(String(50),default='')
    weibo       = Column(String(50),default='')
    instagram   = Column(String(50),default='')
    flickr      = Column(String(50),default='')
    twitter     = Column(String(50),default='')
    renren      = Column(String(50),default='')
    facebook    = Column(String(50),default='')
    weixin      = Column(String(50),default='')
    douban      = Column(String(50),default='')
    other1      = Column(String(50),default='')
    other2      = Column(String(50),default='')
    other3      = Column(String(50),default='')
    other4      = Column(String(50),default='')

    create_time = Column(DateTime,default=datetime.utcnow)

    def __unicode__(self):
        return self.username

    def __init__(self, **kwargs):
        self.token = self.create_token(16)

        if 'password' in kwargs:
            raw = kwargs.pop('password')
            self.password = self.create_password(raw)

        if 'username' in kwargs:
            username = kwargs.pop('username')
            self.username = username.lower()

        if 'email' in kwargs:
            email = kwargs.pop('email')
            self.email = email.lower()

        for k, v in kwargs.items():
            setattr(self, k, v)


    @staticmethod
    def create_password(raw):
        passwd = '%s%s' % (raw, db.app.config['PASSWORD_SECRET'])
        return security.generate_password_hash(passwd)

    @staticmethod
    def create_token(length=16):
        return security.gen_salt(length)

    @property
    def is_admin(self):
        return self.id == 1 

    def check_password(self, raw):
        passwd = '%s%s' % (raw, db.app.config['PASSWORD_SECRET'])
        return security.check_password_hash(self.password, passwd)

    def change_password(self, raw):
        self.password = self.create_password(raw)
        self.token = self.create_token()
        return self


class Looking(db.Model):
    id          = Column(Integer, primary_key = True)
    user_id     = Column(Integer,db.ForeignKey('user.id'),index = True,nullable = False)
    user        = db.relationship('User',lazy='joined',uselist=False)
    age         = Column(Integer,default=30)
    weight      = Column(Integer,default=75)
    height      = Column(Integer,default=175)

    latitude    = Column(Float,default=0,index = True)
    longitude   = Column(Float,default=0,index = True)

    like        = Column(Integer,default=0)
    photo       = Column(String(120),default='')
    
    question1   = Column(String(200),default='')
    question2   = Column(String(200),default='')
    question3   = Column(String(200),default='')
    question4   = Column(String(200),default='')
    question5   = Column(String(200),default='')
    question6   = Column(String(200),default='')

    info        = Column(String(500),default='')

    find_active   = Column(Boolean,default=0)
    server_active = Column(Boolean,default=0)
    active_time   = Column(DateTime,default=datetime.utcnow)

    passinfo      = Column(String(500),default='')

class Node(db.Model):
    '''
    node_type 
    1: 所有人可见
    2: 必须注册才可以看到 
    '''
    id          = Column(Integer, primary_key = True)
    avatar      = Column(String(200),nullable  = False)
    aside       = Column(Text)
    name        = Column(String(40),nullable  = False)
    description = Column(String(400))
    slug        = Column(String(20),nullable  = False,index      = True,unique = True)
    create_time = Column(DateTime,default     = datetime.utcnow)
    node_type   = Column(Integer,default      = 1)

    def __unicode__(self):
        return self.name

class Interview(db.Model):
    id            = Column(Integer, primary_key = True)
    title         = Column(String(140),nullable = False)
    create_time   = Column(DateTime,default     = datetime.utcnow)
    content       = Column(Text)
    hits          = Column(Integer,default      = 0)
    absurl        = Column(String(200),nullable = True,index = True)

    cover = Column(String(400))
    
    def __unicode__(self):
        return self.title

class Page(db.Model):
    id            = Column(Integer, primary_key = True)
    title         = Column(String(140),nullable = False)
    create_time   = Column(DateTime,default     = datetime.utcnow)
    content       = Column(Text)
    hits          = Column(Integer,default      = 0)
    absurl        = Column(String(200),nullable = True,index = True)
    
    cover = Column(String(400))

    def __unicode__(self):
        return self.title

class Topic(db.Model):
    id            = Column(Integer, primary_key = True)
    node_id       = Column(Integer, db.ForeignKey('node.id'),index=True, nullable=False)
    node = db.relationship('Node',lazy='joined')
    user_id       = Column(Integer,db.ForeignKey('user.id'),index = True,nullable = False)
    user = db.relationship('User',lazy='joined')
    title         = Column(String(140),nullable = False)
    create_time   = Column(DateTime,default     = datetime.utcnow)
    update_time   = Column(DateTime,default     = datetime.utcnow)
    content       = Column(Text)
    hits          = Column(Integer,default      = 0)
    comment_count = Column(Integer,default      = 0)
    ip            = Column(String(20),default="")
    
    def __unicode__(self):
        return self.title

class Comment(db.Model):
    id          = Column(Integer, primary_key = True)
    topic_id    = Column(Integer,db.ForeignKey('topic.id'),nullable = False)
    topic = db.relationship('Topic',lazy='joined')
    user_id     = Column(Integer,db.ForeignKey('user.id'),index = True,nullable = False)
    user = db.relationship('User',lazy='joined')
    content     = Column(Text,nullable        = False)
    create_time = Column(DateTime,default     = datetime.utcnow)
    ip          = Column(String(20),default="")

    def __unicode__(self):
        return self.content
    

class FavTopic(db.Model):
    id          = Column(Integer, primary_key = True)
    user_id     = db.Column(db.Integer,index=True, nullable=False)
    topic_id    = db.Column(db.Integer,index=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)


class FavNode(db.Model):
    id          = Column(Integer, primary_key = True)
    user_id     = db.Column(db.Integer,index=True, nullable=False)
    node_id     = db.Column(db.Integer,index=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)


class FavUser(db.Model):
    id          = Column(Integer, primary_key = True)
    user_id     = db.Column(db.Integer,index=True, nullable=False)
    target_id   = db.Column(db.Integer,index=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    ''' 
        n_type 
        1: 回复你
        2: 回复中提到你
        3: 话题中提到你
    '''
    id          = Column(Integer, primary_key = True)
    user_id     = db.Column(db.Integer,index=True, nullable=False)
    action_id   = Column(Integer,db.ForeignKey('user.id'),nullable = False)
    action      = db.relationship('User',lazy='joined')
    n_type      = db.Column(db.Integer, nullable=False)
    title       = Column(String(140),nullable = False)
    topic_id    = db.Column(db.Integer, nullable=False)
    content     = Column(Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)


class TreeHole(db.Model):
    id            = Column(Integer, primary_key = True)
    title         = Column(String(140),nullable = False)
    create_time   = Column(DateTime,default     = datetime.utcnow)
    update_time   = Column(DateTime,default     = datetime.utcnow)
    content       = Column(Text)
    hits          = Column(Integer,default      = 0)
    comment_count = Column(Integer,default      = 0)
    ip            = Column(String(20),default="")
    
    def __unicode__(self):
        return self.title

class TreeComment(db.Model):
    id          = Column(Integer, primary_key = True)
    treehole_id    = Column(Integer,nullable = False)
    content     = Column(Text,nullable        = False)
    create_time = Column(DateTime,default     = datetime.utcnow)
    ip          = Column(String(20),default="")

    def __unicode__(self):
        return self.content
    
