from cherrymoon.ext.db import r
from flask import g

def post_check(ip):
    key = "limit_ip:"+ip
    ip_len = r.llen(key)
    if ip_len > 10:
        #print "to much post"
        key = "bad_user:"+g.user.username
        r.set(key,ip)
        return False
    else:
        if not r.exists(key):
            pipe = r.pipeline()
            pipe.rpush(key,ip)
            pipe.expire(key,60)
            pipe.execute()
        else:
            r.rpushx(key,ip)
        #print "record a ip"
        return True



#post_check("127.0.0.1")

