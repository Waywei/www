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
from cherrymoon import app
from cherrymoon.ext.helper import render ,require_login
from cherrymoon.forms import SignupForm,SigninForm,SettingForm,TopicForm,CommentForm
from cherrymoon.forms import FindingForm,UploadForm
from cherrymoon.redis.fav_topic import *
from cherrymoon.redis.fav_node import *
from cherrymoon.redis.fav_user import *



@app.route('/register',methods=['GET','POST'])
def register():
    if g.user:
        logout()
        return redirect('/register')
    form = SignupForm()        

    if form.validate_on_submit():
        user = User(**form.data)
        db.session.add(user)
        db.session.commit()
        session['id'] = user.id
        session['token'] = user.token
        flash(u'注册成功','success')
        return redirect('/setting')
    return render('/register.jade',locals())

@app.route('/login',methods=['GET','POST'])
def login():
    if g.user:
        flash(u'登陆成功','success')
        return redirect('/setting')
    form = SigninForm()
    if form.validate_on_submit():
        if not form.user:
            return none
        else:
            session.permanent = True
            session['id'] = form.user.id
            session['token'] = form.user.token
            flash(u'登陆成功','success')
            return redirect('/setting')
    return render('/login.jade',locals())

@app.route('/logout')
def logout():
    if not g.user:
        return redirect('/login')
    else:
        session.pop('id')
        session.pop('token')
    return redirect('/login')

@app.route('/setting',methods=['GET','POST'])
@require_login
def setting():
    user = g.user
    form = SettingForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash(u'设置成功','success')
    return render('/setting.jade',locals())

@app.route('/avatar',methods=['GET','POST'])
@require_login
def avatar():
    return render('/avatar.jade',locals())

@app.route('/member/<int:id>')
def memberinfo(id):
    user = User.query.filter_by(id=id).first_or_404()
    if g.user:
        mid = str(g.user.id)
        tid = str(id)
        isFav = user_is_fav(mid,tid)
    else:
        ifFav = None
    return render('/member/member.jade',locals())
    
@app.route('/member/<int:id>/topic')
def membertopic(id):
    user = User.query.filter_by(id=id).first_or_404()
    topics = Topic.query.filter_by(user_id=id).limit(20)
    if g.user:
        mid = str(g.user.id)
        tid = str(id)
        isFav = user_is_fav(mid,tid)
    else:
        ifFav = None

    return render('/member/topic.jade',locals())
    
@app.route('/member/<int:id>/reply')
def memberreply(id):
    user = User.query.filter_by(id=id).first_or_404()
    comments = Comment.query.filter_by(user_id=user.id).limit(20)
    if g.user:
        mid = str(g.user.id)
        tid = str(id)
        isFav = user_is_fav(mid,tid)
    else:
        ifFav = None

    return render('/member/reply.jade',locals())
 
@app.route('/my/favtopic')
@require_login
def memberfavtopic():
    user = g.user
    tid = fav_topic_list(str(g.user.id))
    favtopic = Topic.query.filter(Topic.id.in_(tid)).all()
    return render('/my/fav-topic.jade',locals())

@app.route('/my/favnode')
@require_login
def memberfavnode():
    user = g.user
    tid = fav_node_list(str(g.user.id))
    favnode = Node.query.filter(Node.id.in_(tid)).all()
    return render('/my/fav-node.jade',locals())

@app.route('/my/favuser')
@require_login
def memberfavmember():
    user = g.user
    tid = fav_user_list(str(g.user.id))
    favuser = User.query.filter(User.id.in_(tid)).all()
    return render('/my/fav-member.jade',locals())
