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


@manager.command
def runserver():
    #app.run("192.168.1.126")
    app.run()

@manager.command
def syncdb():
    db.create_all() 


if __name__ == "__main__":
    manager.run()

