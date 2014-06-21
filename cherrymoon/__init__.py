# -*- coding: utf-8 -*-  
from flask import Flask, g 
from flask import request,g
from flask import session
from flask import redirect
app = Flask(__name__,static_folder="public")
from ext.db import db
from ext.helper import get_current_user,generate_csrf_token
from ext.helper import is_admin
from timeit import default_timer

import cherrymoon.ext.tpl_filter
import cherrymoon.view.view
import cherrymoon.view.user
#import cherrymoon.view.find
import cherrymoon.view.talk
import cherrymoon.view.admin

import cherrymoon.view.sapi
from cherrymoon.redis.limiter import post_check

app.config.from_object('cherrymoon.config')

db.init_app(app)
db.app = app

@app.before_request
def load_current_user():
    g.user = get_current_user()
    g.starttimer = default_timer()
    g.admin = is_admin()
    #print g.user
    #check if to much post
    if request.method == 'POST' and g.user:
        ip = str(request.remote_addr)
        limit = post_check(ip)
        if not limit:
            return u"你对服务器提交数据的频率过快，系统已经记录了你用户名，这种行为将会导致账号被ban"

    

@app.after_request
def request_time(response):
    timer = str(default_timer()-g.starttimer)
    try:
        response.data = response.data.replace("<-timer->",timer)
    except:
        pass
    return response

app.jinja_env.globals['csrf_token'] =generate_csrf_token
#pyjade templete
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


if __name__ == '__main__':
    app.run()

