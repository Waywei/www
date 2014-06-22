# -*- coding: utf-8 -*-  
from flask import flash,render_template, redirect,url_for
from flask import g,request,flash,session
from flask import abort
from flask import Response
from datetime import *
from cherrymoon.ext.db import db,r
from cherrymoon.ext.helper import k
from cherrymoon.ext.helper import csrf_check
from cherrymoon.models import User, Node, Topic, Comment, Interview 
from cherrymoon.models import Page,Notification
from cherrymoon.models import FavUser, FavNode, FavTopic
from cherrymoon import app
from cherrymoon.ext.helper import render ,require_login
from cherrymoon.forms import SignupForm,SigninForm,SettingForm,TopicForm,CommentForm
import re
from cherrymoon.redis.counter import Counter

notify = Counter()

def r_set (key,val,sec):
    pipe = r.pipeline()
    pipe.set(key,val)
    pipe.expire(key,sec)
    pipe.execute()

@app.route('/interview/atom.xml')
def interview_atom():
    xml = r.get("feed:interview")
    if not xml:
        interviews = Interview.query\
                .order_by(Interview.create_time.desc()).limit(10).all()
        site = k()
        site.title= u"bearwave 访谈"
        site.subtitle = u"不同的生活经历,得到不同的生活经验,把他们留给年轻人是一件非常有意义的事情"
        site.url = u"http://www.bearwave.com/interview"
        site.atomurl = u"http://www.bearwave.com/interview/atom.xml"
        site.topics = interviews
        site.time = datetime.now()
        xml =  render('/feed/interview.xml',locals())
        r_set("feed:interview",xml,60*60)
    return Response(xml, mimetype='text/xml')

@app.route('/atom.xml')
def topic_atom():
    xml = r.get("feed:topic")
    if not xml:
        topics = Topic.query\
                .order_by(Topic.create_time.desc()).limit(10).all()
        site = k()
        site.title= u"bearwave 话题"
        site.subtitle = u"最近的话题"
        site.url = u"http://www.bearwave.com"
        site.atomurl = u"http://www.bearwave.com/atom.xml"
        site.topics = topics
        site.time = datetime.now()
        xml =  render('/feed/topic.xml',locals())
        r_set("feed:topic",xml,60*60)
    return Response(xml, mimetype='text/xml')

@app.route('/')
def index():
    topics = Topic.query.order_by(Topic.update_time.desc()).limit(10).all()
    interviews = Interview.query\
            .order_by(Interview.create_time.desc()).limit(4).all()
    nodelist = [1,2,3,4,5,8]
    node = Node.query.filter(Node.id.in_(nodelist))
    return render('/index.jade',locals())

@app.route('/node')
def node_view():
    nodes =Node.query.order_by(Node.id.desc()).all()
    return render('/node.jade',locals())

@app.route('/recent')
@app.route('/recent/page/<int:page>')
def recent_topic(page=1):
    try:
        topics = Topic.query.order_by(Topic.update_time.desc())\
            .paginate(page,per_page=30)
    except:
        topics = None
    return render('/recent.jade',locals())

@app.route('/node/<slug>')
@app.route('/node/<slug>/page/<int:page>')
def topic_list(slug,page=1):
    try:
        node = Node.query.filter_by(slug=slug).first_or_404()
        if not g.user and node.node_type == 2:
            flash(u"当前节点是私密的节点，需要登陆后才可以访问","warning")
            return redirect("/login")

        node.topic_count = Topic.query.filter_by(node_id=node.id).count() 
        if g.user:
            mid = str(g.user.id)
            tid = str(node.id)
            isFav = FavNode.query.filter_by(user_id=mid, node_id=tid).first()
        topics = Topic.query.filter_by(node_id=node.id)\
            .order_by(Topic.update_time.desc()).paginate(page,per_page=30)
    except:
        isFav = None
        topics = None
        node = None
    return render('/node/node.jade',locals())

@app.route('/node/<slug>/new',methods=['GET','POST'])
@require_login
def topic_add(slug):
    form = TopicForm()
    node = Node.query.filter_by(slug=slug).first();
    node.topic_count = Topic.query.filter_by(node_id=node.id).count() 

    if form.validate_on_submit():
        topic = Topic(**form.data)
        topic.content = topic.content.strip()
        topic.node = node
        topic.user = g.user
        topic.ip = request.remote_addr
        
        db.session.add(topic)
        db.session.commit()

        #Notification
        users = notiuser(topic.content)
        #print users
        if len(users) > 0 :
            for u in users:
                n = Notification(user_id= u.id,
                        action=g.user,
                        n_type=3,
                        title=topic.title,
                        topic_id=topic.id,
                        content=topic.content)
                notify.incr("notify:user%s" % u.id)
                db.session.add(n)
                db.session.commit()
 
        return redirect('/topic/'+str(topic.id))
    return render('/node/new.jade',locals())

def notiuser(content):
    nlist = re.findall('@[_a-zA-Z0-9]+\s?',content)
    ulist = list()
    for n in nlist:
        username = n.strip().replace("@","")
        ulist.append(username)
    users = User.query.filter(User.username.in_(ulist)).all()
    return users


@app.route('/topic/<int:topic_id>',methods=['GET','POST'])
def topic_detail(topic_id):
    topic = Topic.query.get_or_404(topic_id)

    if not g.user and topic.node.node_type == 2:
        flash(u"当前话题属于私密节点,需要登陆后才可以访问","warning")
        return redirect("/login")

    node = Node.query.filter_by(id= topic.node_id).first()
    topic.hits += 1
    db.session.commit()
    comments = Comment.query.filter_by(topic_id=topic_id)\
        .order_by(Comment.create_time)
    form = None
    isFav = None
    if g.user:
        mid = str(g.user.id)
        tid = str(topic_id)
        isFav = FavTopic.query.filter_by(user_id=mid, topic_id=tid).first()
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(**form.data)
            comment.content = comment.content.strip()
            comment.topic = topic
            comment.user = g.user
            comment.ip   = request.remote_addr
            topic.update_time = datetime.now()
            topic.comment_count += 1

            #Notification
            if g.user.id != topic.user_id:
                n = Notification(
                    user_id= topic.user_id,
                    action_id = g.user.id,
                    n_type = 1,
                    title = topic.title,
                    topic_id= topic.id,
                    content = comment.content
                    )
                db.session.add(n)
                notify.incr("notify:user%s" % topic.user_id)
            
            users = notiuser(comment.content)
            if len(users) > 0:
                for user in users:
                    noti = Notification(
                        user_id= user.id,
                        action_id = g.user.id,
                        n_type = 2,
                        title = topic.title,
                        topic_id = topic.id,
                        content = comment.content
                        )
                    db.session.add(noti)
                    notify.incr("notify:user%s" % user.id)
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

@app.route('/notification')
@app.route('/notification/<int:page>')
@require_login
def notification(page=1):
    notis = Notification.query.filter_by(user_id=g.user.id)\
            .order_by(Notification.create_time.desc()).paginate(page,per_page=20)
    notify.reset("notify:user%s" % g.user.id)
    return render('notification.jade',locals())
