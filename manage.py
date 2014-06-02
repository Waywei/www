from cherrymoon import app
from flask.ext.script import Manager
from cherrymoon.ext.db import db
from cherrymoon.ext.helper import send_email

manager = Manager(app)


@manager.command
def runserver():
    #app.run("192.168.1.126")
    app.run()

@manager.command
def syncdb():
    db.create_all() 

@manager.command
def testmail():
    send_email('syllormore@gmail.com','tttttt','dwqdwqdqw dwq d wqdwq ')


if __name__ == "__main__":
    manager.run()

