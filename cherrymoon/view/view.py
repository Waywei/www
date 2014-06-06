# -*- coding: utf-8 -*-  
from flask import flash,render_template, redirect,url_for
from flask import g,request,flash,session
from flask import abort
from datetime import *
from cherrymoon.ext.db import db,r
from cherrymoon.ext.helper import k
from cherrymoon.ext.helper import csrf_check
from cherrymoon.models import User, Node, Topic, Comment, Interview 
from cherrymoon.models import Page
from cherrymoon.models import FavUser, FavNode, FavTopic
from cherrymoon import app
from cherrymoon.ext.helper import render ,require_login
from cherrymoon.forms import SignupForm,SigninForm,SettingForm,TopicForm,CommentForm
from cherrymoon.forms import FindingForm,UploadForm


@app.route('/')
def index():
    topics = Topic.query.order_by(Topic.update_time.desc()).limit(10)
    interviews = Interview.query\
            .order_by(Interview.create_time.desc()).limit(10)
    node = Node.query.order_by(Node.create_time).limit(30)
    return render('/index.jade',locals())

@app.route('/node')
def node_view():
    nodes =Node.query.order_by(Node.id.desc()).all()
    return render('/node.jade',locals())

@app.route('/recent')
@app.route('/recent/page/<int:page>')
def recent_topic(page=1):
    try:
        show_node_type = (1,2)
        show_nodes = Node.query.filter(Node.node_type.in_(show_node_type)).all()
        showid = [x.id for x in show_nodes]
        topics = Topic.query.filter(Topic.node_id.in_(showid))\
            .order_by(Topic.update_time.desc()).paginate(page,per_page=20)
    except:
        topics = None
    return render('/recent.jade',locals())

@app.route('/node/<slug>')
@app.route('/node/<slug>/page/<int:page>')
def topic_list(slug,page=1):
    try:
        node = Node.query.filter_by(slug=slug).first_or_404()
        node.topic_count = Topic.query.filter_by(node_id=node.id).count() 
        if g.user:
            mid = str(g.user.id)
            tid = str(node.id)
            isFav = FavNode.query.filter_by(user_id=mid, node_id=tid).first()
        topics = Topic.query.filter_by(node_id=node.id)\
            .order_by(Topic.update_time.desc()).paginate(page,per_page=20)
    except:
        isFav = None
        topics = None
    return render('/node/node.jade',locals())

@app.route('/node/<slug>/new',methods=['GET','POST'])
@require_login
def topic_add(slug):
    form = TopicForm()
    node = Node.query.filter_by(slug=slug).first();
    node.topic_count = Topic.query.filter_by(node_id=node.id).count() 
    if form.validate_on_submit():
        topic = Topic(**form.data)
        topic.node = node
        topic.user = g.user
        topic.ip = request.remote_addr
        db.session.add(topic)
        db.session.commit()
        return redirect('/topic/'+str(topic.id))
    return render('/node/new.jade',locals())

@app.route('/topic/<int:topic_id>',methods=['GET','POST'])
def topic_detail(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    node = Node.query.filter_by(id= topic.node_id).first()
    topic.hits += 1
    db.session.commit()
    comments = Comment.query.filter_by(topic_id=topic_id)
    form = None
    isFav = None
    if g.user:
        mid = str(g.user.id)
        tid = str(topic_id)
        isFav = FavTopic.query.filter_by(user_id=mid, topic_id=tid).first()
    if g.user:
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(**form.data)
            comment.topic = topic
            comment.user = g.user
            comment.ip   = request.remote_addr
            topic.update_time = datetime.now()
            topic.comment_count += 1
            db.session.add(comment)
            db.session.commit()
            count = comments.count()
            return redirect('/topic/'+str(topic.id)+'#comment-'+str(count))
    return render('/node/topic.jade',locals())

@app.route('/test',methods=('GET','POST'))
def test():
    namefield = k()
    if request.method == "POST":
        csrf_check()
        namefield.text = request.form["name"]
        if not namefield.text or len(namefield.text) > 20:
            namefield.error = u"not empty"

    return render('test.jade',locals())
