# -*- coding: utf-8 -*-  
from flask import flash,render_template, redirect,url_for
from flask import g,request,flash,session
from flask import abort
from datetime import *
from cherrymoon.ext.db import db,r
from cherrymoon.ext.helper import k
from cherrymoon.ext.helper import csrf_check
from cherrymoon.models import User, Node, Topic, Comment, Interview 
from cherrymoon.models import Find
from cherrymoon.models import Page
from cherrymoon import app
from cherrymoon.ext.helper import render ,require_login
from cherrymoon.forms import SignupForm,SigninForm,SettingForm,TopicForm,CommentForm
from cherrymoon.forms import FindingForm,UploadForm
from werkzeug import secure_filename
from PIL import Image,ImageOps
import os
import uuid



@app.route('/find')
@app.route('/find/page/<int:page>',methods=['GET','POST'])
@require_login
def find_all(page=1):
    members = Find.query.filter_by(server_active="1",find_active="1")\
            .paginate(page,per_page=20)

    return render('/find.jade',locals())


@app.route('/find/setting',methods=['GET','POST'])
@require_login
def find_setting():
    user = g.user
    form = FindingForm(obj=user)
    uploadform = UploadForm()
    if form.validate_on_submit():
        user.server_active = 0
        user.active_time = datetime.now()
        form.populate_obj(user)
        db.session.commit()
        flash(u'设置成功,等待人工审核信息','success')
    return render('/find/setting.jade',locals())

@app.route('/find/upload',methods=['POST'])
@require_login
def findupload():
    form = UploadForm()
    if form.validate_on_submit():
        try:
            filename = secure_filename(form.uploads.data.filename)
            rid = str(uuid.uuid4())
            fname = rid+'.jpg'
            UPLOAD_FOLDER = 'cherrymoon/public/upload/find'
            img = Image.open(form.uploads.data)
            imgfit = ImageOps.fit(img,(500,500),Image.ANTIALIAS)
            imgfit.save(os.path.join(UPLOAD_FOLDER, fname),quality=100)
            user = User.query.filter_by(id=g.user.id).first_or_404()
            user.photo = rid+'.jpg'
            user.server_active = 0
            user.active_time = datetime.now()
            db.session.commit()
            flash(u'更新头像成功,等待人工审核信息','success')
            return redirect('/find/setting') 
        except:
            return u"别乱搞啊"
