from cherrymoon import app
from flask import g,request,jsonify
from cherrymoon.ext.db import db
from cherrymoon.models import FavTopic, FavUser, FavNode
from cherrymoon.ext.helper import require_login

@app.route('/api/v1/fav/user/<int:target>',methods=['POST'])
@require_login
def user(target):
    myid = g.user.id
    tid = str(target)
    fav = FavUser.query.filter_by(user_id=myid,target_id=tid).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify(action="unfav")
    else:
        favuser = FavUser(user_id=myid,target_id=tid)
        db.session.add(favuser)
        db.session.commit()
        return jsonify(action="fav")

@app.route('/api/v1/fav/node/<int:target>',methods=['POST'])
@require_login
def node(target):
    myid = str(g.user.id)
    tid = str(target)
    fav = FavNode.query.filter_by(user_id=myid,node_id=tid).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify(action="unfav")
    else:
        favnode = FavNode(user_id=myid,node_id=tid)
        db.session.add(favnode)
        db.session.commit()
        return jsonify(action="fav")

@app.route('/api/v1/fav/topic/<int:target>',methods=['POST'])
@require_login
def topic(target):
    myid = str(g.user.id)
    tid = str(target)
    fav = FavTopic.query.filter_by(user_id=myid,topic_id=tid).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify(action="unfav")
    else:
        favtopic = FavTopic(user_id=myid,topic_id=tid)
        db.session.add(favtopic)
        db.session.commit()
        return jsonify(action="fav")

@app.route('/api/v1/uploadavatar',methods=['GET','POST'])
def uploadavatar():
    if not g.user:
        return "stop fuck with me"
    else:
        try:
            data = request.form['url']
            g.user.avatar = data 
            db.session.commit()
            return jsonify(action="ok")
        except:
            return jsonify(action="error")
