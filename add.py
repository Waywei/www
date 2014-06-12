from flask import Flask, g 
app = Flask(__name__,static_folder="public")
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.init_app(app)
app.config.from_object('cherrymoon.config')

manager = Manager(app)

class TreeHole(db.Model):
    id            = db.Column(db.Integer, primary_key = True)
    title         = db.Column(db.String(140),nullable = False)
    
    def __unicode__(self):
        return self.title



@manager.command
def runserver():
    #app.run("192.168.1.126")
    app.run()

@manager.command
def syncdb():
    db.create_all() 


if __name__ == "__main__":
    manager.run()

