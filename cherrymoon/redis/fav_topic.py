from cherrymoon.ext.db import r

def fav_topic(mid,tid):
    fav_status = r.sadd('fav_topic:'+mid,tid)
    faved_status = r.sadd('faved_topic:'+tid,mid)
    return fav_status and faved_status

def unfav_topic(mid,tid):
    fav_status = r.srem('fav_topic:'+mid,tid)
    faved_status = r.srem('faved_topic:'+tid,mid)
    return fav_status and faved_status

def fav_topic_list(mid):
    return r.smembers('fav_topic:'+mid)

def fav_topic_count(mid):
    return r.scard('fav_topic:'+mid)

def faved_topic_list(mid):
    return r.smembers('faved_topic:'+mid)

def faved_topic_count(mid):
    return r.scard('faved_topic:'+mid)

def topic_is_fav(mid,tid):
    return r.sismember('fav_topic:'+mid,tid)

def topic_is_faved(mid,tid):
    return r.sismember('fav_topic:'+tid,mid)


#unfav_topic("1","2")

#aaa = fav_topic_list("1")
#aaa = fav_topic_count("333")
#aaa = topic_is_fav("333","999")
#aaa = topic_is_faved("999","333")
#print aaa
