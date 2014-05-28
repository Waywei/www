from cherrymoon import app
from flask import g,request,jsonify
from cherrymoon.redis.fav_user import user_is_fav,fav_user,unfav_user
from cherrymoon.redis.fav_node import node_is_fav,fav_node,unfav_node
from cherrymoon.redis.fav_topic import topic_is_fav,fav_topic,unfav_topic
from cherrymoon.ext.helper import require_login

@app.route('/api/v1/fav/user/<int:target>',methods=['GET','POST'])
@require_login
def user(target):
    mid = str(g.user.id)
    tid = str(target)
    if user_is_fav(mid,tid):
        unfav_user(mid,tid)
        return jsonify(action="unfav")
    else:
        fav_user(mid,tid)
        return jsonify(action="fav")

@app.route('/api/v1/fav/node/<int:target>',methods=['GET','POST'])
@require_login
def node(target):
    mid = str(g.user.id)
    tid = str(target)
    if node_is_fav(mid,tid):
        unfav_node(mid,tid)
        return jsonify(action="unfav")
    else:
        fav_node(mid,tid)
        return jsonify(action="fav")

@app.route('/api/v1/fav/topic/<int:target>',methods=['GET','POST'])
@require_login
def topic(target):
    mid = str(g.user.id)
    tid = str(target)
    if topic_is_fav(mid,tid):
        unfav_topic(mid,tid)
        return jsonify(action="unfav")
    else:
        fav_topic(mid,tid)
        return jsonify(action="fav")


