from cherrymoon import app
from flask.ext.script import Manager
from cherrymoon.ext.db import db

manager = Manager(app)


@manager.command
def runserver():
    #app.run("192.168.1.126")
    app.run()

@manager.command
def syncdb():
    db.create_all() 


if __name__ == "__main__":
    manager.run()

