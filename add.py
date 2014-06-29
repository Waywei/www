from flask import Flask, g 
app = Flask(__name__,static_folder="public")
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime
from sqlalchemy import Float
from datetime import datetime

db = SQLAlchemy()
db.init_app(app)
app.config.from_object('cherrymoon.config')

manager = Manager(app)



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
    age         = Column(Integer)
    weight      = Column(Integer)
    height      = Column(Integer)

    latitude    = Column(Float,default=0,index = True)
    longitude   = Column(Float,default=0,index = True)

    like        = Column(Integer,default=0)
    photo       = Column(String(120),default="")
    
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


@manager.command
def runserver():
    #app.run("192.168.1.126")
    app.run()

@manager.command
def syncdb():
    db.create_all() 


if __name__ == "__main__":
    manager.run()

