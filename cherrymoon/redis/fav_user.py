from cherrymoon.ext.db import r

def fav_user(mid,tid):
    fav_status = r.sadd('fav_user:'+mid,tid)
    faved_status = r.sadd('faved_user:'+tid,mid)
    return fav_status and faved_status

def unfav_user(mid,tid):
    fav_status = r.srem('fav_user:'+mid,tid)
    faved_status = r.srem('faved_user:'+tid,mid)
    return fav_status and faved_status

def fav_user_list(mid):
    return r.smembers('fav_user:'+mid)

def fav_user_count(mid):
    return r.scard('fav_user:'+mid)

def faved_user_list(mid):
    return r.smembers('faved_user:'+mid)

def faved_user_count(mid):
    return r.scard('faved_user:'+mid)

def user_is_fav(mid,tid):
    return r.sismember('fav_user:'+mid,tid)

def user_is_faved(mid,tid):
    return r.sismember('fav_user:'+tid,mid)


#unfav_user("1","2")
#fav_user("333","999")
#aaa = fav_user_list("1")
#aaa = fav_user_count("333")
#aaa = user_is_faved("999","333")
#if user_is_fav("333","999"):
    #print "ok"
#else: 
    #print "okokok"
