# -*- coding: utf-8 -*-  
from flask import render_template
from cherrymoon.models import User
from flask import session, abort
from flask import request, g
import functools
from flask import redirect,flash
from cherrymoon.ext.db import db,r
from uuid import uuid4
from cherrymoon.redis.counter import Counter
notify = Counter()
import requests

admin_list = [1,2,3]

def render(tmp,items):
    return render_template(tmp,**items)

def get_current_user():
    if 'id' in session and 'token' in session:
        user = User.query.get(int(session['id']))
        if not user:
            return None
        if user.token != session['token']:
            return None
        user.notify = notify.get("notify:user%s" % user.id) 
        return user
    return None

def require_login(f):
    @functools.wraps(f)
    def wrapper(*args,**kw):
        if not g.user:
            flash(u'需要登陆才可以访问','warning')
            return redirect('/login')
        return f(*args,**kw)
    return wrapper

def require_admin(f):
    @functools.wraps(f)
    def wrapper(*args,**kw):
        if not g.user and g.user.id in admin_list:
            return redirect('/')
        return f(*args,**kw)
    return wrapper

def is_admin():
    try:
        if g.user and g.user.id in admin_list:
            return True
    except:
        return False

class k(object):
    pass

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid4()
    return session['_csrf_token']

def csrf_check():
    token = str(session.pop('_csrf_token',None))
    if not token or token != request.form["_csrf_token"]:
        abort(403)

def send_email(to,subject,text):
    requests.post(
        "https://api.mailgun.net/v2/bearwave.com/messages",
        auth=("api", db.app.config['MAILGUN']),
        data={"from": "bearwave <postmaster@bearwave.com>",
              "to": [to],
              "subject": subject,
              "text": text})


