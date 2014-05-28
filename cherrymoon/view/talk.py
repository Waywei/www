# -*- coding: utf-8 -*-  
from flask import flash,render_template, redirect,url_for
from flask import g,request,flash,session
from flask import abort
from datetime import *
from cherrymoon.ext.db import db,r
from cherrymoon.ext.helper import k
from cherrymoon.models import User, Node, Topic, Comment, Interview 
from cherrymoon.models import Page
from cherrymoon import app
from cherrymoon.ext.helper import render ,require_login

@app.route('/interview')
@app.route('/interview/page/<int:page>')
def interview(page=1):
    interviews = Interview.query\
            .order_by(Interview.create_time.desc())\
            .paginate(page,per_page=10)
    return render('/interview.jade',locals())

@app.route('/interview/<url>')
def interview_details(url):
    interview = Interview.query.filter_by(absurl=url).first_or_404()
    return render('/interview-details.jade',locals())

@app.route('/page/<url>')
def page_details(url):
    interview = Page.query.filter_by(absurl=url).first_or_404()
    return render('/page.jade',locals())

