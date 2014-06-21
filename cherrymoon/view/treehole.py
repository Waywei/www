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
from cherrymoon.models import TreeHole, TreeComment
from cherrymoon import app
from cherrymoon.ext.helper import render ,require_login
from cherrymoon.forms import TreeHoleForm,TreeCommentForm
import re

@app.route('/treehole')
@app.route('/treehole/page/<int:page>')
def recent_treehole(page=1):
    try:
        topics = TreeHole.query.order_by(TreeHole.update_time.desc())\
            .paginate(page,per_page=30)
    except:
        topics = None
    return render('/TreeHole/list.jade',locals())



@app.route('/treehole/new',methods=['GET','POST'])
@require_login
def treehole_add():
    form = TreeHoleForm()
    if form.validate_on_submit():
        th = TreeHole(**form.data)
        th.content = th.content.strip()
        th.ip = request.remote_addr
        db.session.add(th)
        db.session.commit()

        return redirect('/treehole/'+str(th.id))
    return render('/treehole/new.jade',locals())


@app.route('/treehole/<int:id>',methods=['GET','POST'])
def treehole_detail(id):
    th = TreeHole.query.get_or_404(id)
    th.hits += 1
    db.session.commit()
    comments = TreeComment.query.filter_by(treehole_id=id)\
        .order_by(TreeComment.create_time).all()
    print "xxxxxx"
    for c in comments:
        print c
    form = None
    if g.user:
        form = TreeCommentForm()
        if form.validate_on_submit():
            comment = TreeComment(**form.data)
            comment.content = comment.content.strip()
            comment.treehole_id  = id
            comment.ip   = request.remote_addr
            th.update_time = datetime.now()
            th.comment_count += 1

            db.session.add(comment)
            db.session.commit()
            count = th.comment_count
            return redirect('/treehole/'+str(th.id)+'#comment-'+str(count))
    return render('/treehole/detail.jade',locals())


