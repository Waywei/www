# -*- coding: utf-8 -*-  
from flask import flash,render_template, redirect,url_for
from flask import g,request,flash,session
from flask import abort
from datetime import *
from cherrymoon.ext.db import db,r
from cherrymoon.ext.helper import k, send_email
from cherrymoon.ext.helper import csrf_check
from cherrymoon.models import User, Node, Topic, Comment, Interview 
from cherrymoon.models import Page
from cherrymoon import app
from cherrymoon.ext.helper import render ,require_login
from cherrymoon.forms import SignupForm,SigninForm,SettingForm,TopicForm,CommentForm
from cherrymoon.forms import ForgetForm,ResetPasswordForm
from cherrymoon.models import FavUser, FavTopic, FavNode
from uuid import uuid4
import requests
from gravatar import Gravatar

from qiniu import rs,conf

@app.route('/register',methods=['GET','POST'])
def register():
    if g.user:
        logout()
        return redirect('/register')
    form = SignupForm()        

    if form.validate_on_submit():
        user = User(**form.data)
        imgurl = Gravatar(user.email, secure=False, size=100, rating='x')\
                .thumb+'&d=404'
        req = requests.get(imgurl)
        #print "qqqqq"
        #print req.status_code
        if req.status_code == 200:
            user.avatar = "gravatar"
        db.session.add(user)
        db.session.commit()
        session['id'] = user.id
        session['token'] = user.token
        flash(u'注册成功','success')
        return redirect('/member/'+str(user.id))
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
        return redirect('/member/'+str(g.user.id))
    return render('/setting.jade',locals())

@app.route('/avatar',methods=['GET','POST'])
@require_login
def avatar():
    conf.ACCESS_KEY = app.config["QINIU_ACCESS_KEY"]
    conf.SECRET_KEY = app.config["QINIU_SECRET_KEY"]
    policy = rs.PutPolicy("bearwave")
    qiniutoken = policy.token()
    return render('/avatar.jade',locals())


@app.route('/forgetpassword',methods=['GET','POST'])
def forgetpassword():
    form = ForgetForm()
    if form.validate_on_submit():
        email = form.data['email'].lower()
        name = form.data['username'].lower()
        try:
            user = User.query.filter_by(email = email).first()
        except:
            user = None
        if user and user.username == name:
            result = r.get("resetuser:%s" % email)
            if result:
                finished = k()
                finished.title = u"重新设置密码"
                finished.content = u"重新设置密码的功能在24小时只能使用一次"
                return render('finished.jade',locals())

            uuid = uuid4() 
            pipe = r.pipeline()
            pipe.set("reset:%s" % uuid,email)
            pipe.expire("reset:%s" % uuid,60*60*24)
            pipe.set("resetuser:%s" % email,"1")
            pipe.expire("resetuser:%s" % email,60*60*24)
            pipe.execute()

            subject = u"重新设置密码-BEARWAVE"
            reseturl = "http://www.bearwave.com/resetpassword/"+str(uuid) 
            text = '''

            这是一封系统自动发送的邮件，不能直接回复。
            如果当前操作不是您本人的所为，请忽略这个邮件，但这类操作意味着可能有人对您的隐私有兴趣。

            修改密码可以访问下面的连接
            '''
            msg = text+reseturl
            send_email(email,subject,msg)
            finished = k()
            finished.title = u"重新设置密码"
            finished.content = u"邮件已发送，请注意垃圾邮件箱"
            return render('finished.jade',locals())
        else:
            error = u"邮箱与用户名不匹配"

    return render('/forgetpassword.jade',locals())


@app.route('/resetpassword/<uuid>',methods=['GET','POST'])
def resetpassword(uuid):
    uid = str(uuid)
    mail = r.get("reset:%s" % uuid)
    if mail:
        form = ResetPasswordForm();
        if form.validate_on_submit():
            user = User.query.filter_by(email=mail).first_or_404()
            user.change_password(form.password.data)
            db.session.commit()
            flash(u"密码修改成功",'success')
            return redirect("/login")

        return render('resetpassword.jade',locals())
        
    else:
        return u"您的链接已经过期，发送后24小时内使用才有效"
@app.route('/m/<username>')
def memberslug(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return redirect("/member/"+str(user.id),code=301)
    else:
        return "这个用户不存在"

@app.route('/member/<int:id>')
def memberinfo(id):
    user = User.query.filter_by(id=id).first_or_404()
    if g.user:
        mid = str(g.user.id)
        tid = str(id)
        isFav = FavUser.query.filter_by(user_id=mid, target_id=tid).first()
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
        isFav = FavUser.query.filter_by(user_id=mid, target_id=tid).first()
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
        isFav = FavUser.query.filter_by(user_id=mid, target_id=tid).first()
    else:
        ifFav = None

    return render('/member/reply.jade',locals())
 
@app.route('/my/favtopic')
@require_login
def memberfavtopic():
    user = g.user
    favs = FavTopic.query.filter_by(user_id=user.id).limit(30)
    tid = [x.topic_id for x in favs]
    favtopic = Topic.query.filter(Topic.id.in_(tid)).all()
    return render('/my/fav-topic.jade',locals())

@app.route('/my/favnode')
@require_login
def memberfavnode():
    user = g.user
    favs = FavNode.query.filter_by(user_id=user.id).limit(30)
    tid = [x.node_id for x in favs]
    favnode = Node.query.filter(Node.id.in_(tid)).all()
    return render('/my/fav-node.jade',locals())

@app.route('/my/favuser')
@require_login
def memberfavmember():
    user = g.user
    favs = FavUser.query.filter_by(user_id=user.id).limit(30)
    tid = [x.target_id for x in favs]
    favuser = User.query.filter(User.id.in_(tid)).limit(30)
    return render('/my/fav-member.jade',locals())
