# -*- coding: utf-8 -*-  
from flask import flash,render_template, redirect,url_for
from flask import g,request,flash,session
from flask import abort
from datetime import *
from cherrymoon.ext.db import db,r
from cherrymoon.ext.helper import k
from cherrymoon.ext.helper import csrf_check
from cherrymoon.models import User, Node, Topic, Comment, Interview 
from cherrymoon.models import Looking
from cherrymoon.models import Page
from cherrymoon import app
from cherrymoon.ext.helper import render ,require_login
from cherrymoon.forms import LookingForm
#from werkzeug import secure_filename
#from PIL import Image,ImageOps
from qiniu import conf, rs
import os
import uuid

@app.route('/looking')
@app.route('/looking/page/<int:page>',methods=['GET','POST'])
def find_all(page=1):
    looking = Looking.query.filter_by(server_active="1",find_active="1")\
        .order_by(Looking.active_time.desc())\
        .paginate(page,per_page=20)

    return render('/looking/index.jade',locals())


@app.route('/looking/setting',methods=['GET','POST'])
@require_login
def find_setting():
    user = g.user
    look = Looking.query.filter_by(user_id=user.id).first()
    form = LookingForm(obj=look)
    conf.ACCESS_KEY = app.config["QINIU_ACCESS_KEY"]
    conf.SECRET_KEY = app.config["QINIU_SECRET_KEY"]
    policy = rs.PutPolicy("bearwave")
    qiniutoken = policy.token()
    if form.validate_on_submit():
        if not look:
            look = Looking(**form.data)
            look.user = g.user
            look.server_active = True
            look.active_time = datetime.now()
            db.session.add(look)
            db.session.commit()
            return redirect("/member/"+str(user.id)+"#looking-info")
        else:
            form.populate_obj(look)
            look.server_active = True
            look.active_time = datetime.now()
            db.session.commit()
            return redirect("/member/"+str(user.id)+"#looking-info")

    return render('/looking/setting.jade',locals())


@app.route('/looking/instagram')
@app.route('/looking/instagram/page/<int:page>',methods=['GET','POST'])
def find_instagram(page=1):
    members = User.query.filter(User.instagram!="")\
        .order_by(User.create_time.desc())\
        .paginate(page,per_page=20)
    return render('/looking/instagram.jade',locals())


@app.route('/looking/twitter')
@app.route('/looking/twitter/page/<int:page>',methods=['GET','POST'])
def find_twitter(page=1):
    members = User.query.filter(User.twitter!="")\
        .order_by(User.create_time.desc())\
        .paginate(page,per_page=20)
    return render('/looking/twitter.jade',locals())
