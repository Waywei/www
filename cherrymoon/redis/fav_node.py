from cherrymoon.ext.db import r

def fav_node(mid,tid):
    fav_status = r.sadd('fav_node:'+mid,tid)
    faved_status = r.sadd('faved_node:'+tid,mid)
    return fav_status and faved_status

def unfav_node(mid,tid):
    fav_status = r.srem('fav_node:'+mid,tid)
    faved_status = r.srem('faved_node:'+tid,mid)
    return fav_status and faved_status

def fav_node_list(mid):
    return r.smembers('fav_node:'+mid)

def fav_node_count(mid):
    return r.scard('fav_node:'+mid)

def faved_node_list(mid):
    return r.smembers('faved_node:'+mid)

def faved_node_count(mid):
    return r.scard('faved_node:'+mid)

def node_is_fav(mid,tid):
    return r.sismember('fav_node:'+mid,tid)

def node_is_faved(mid,tid):
    return r.sismember('fav_node:'+tid,mid)


#unfav_node("1","2")

#aaa = fav_node_list("1")
#aaa = fav_node_count("333")
#aaa = node_is_fav("333","999")
#aaa = node_is_faved("999","333")
#print aaa
