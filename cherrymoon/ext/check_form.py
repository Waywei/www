# -*- coding: utf-8 -*-  
import re
def is_email(string):
    emial = re.compile(r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}").match(string)
    if email:
        return True
    else:
        return False

