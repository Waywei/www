from cherrymoon.ext.db import r

class Counter(object):
    def incr(self,counter, increment=1):
        return r.incrby( counter, increment)

    def decr(self,counter, decrement=1):
        return r.decrby( counter, -decrement)

    def get(self,counter):
        value = r.get(counter)
        if value:
            return value
        else:
            return False

    def reset(self,counter):
        value = r.set( counter, 0)
        return False

#notify = Counter()
#notify.incr("notify:user1")
#x = notify.get("notify:user1")
