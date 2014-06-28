# -*- coding: utf-8 -*-  
from cherrymoon import app
import re
import datetime
import string
from jinja2 import escape
from gravatar import Gravatar

@app.template_filter('avatar')
def avatar(user):
    if user.avatar == "gravatar":
        img =  Gravatar(user.email, secure=False, size=100, rating='x').thumb
        return "<img src='%s'/>" % img
    elif user.avatar == "":
        img = app.config['AVATAR']
        return "<img src='%s'/>" % img 
    else:
        img =  app.config['QINIU_URL']+user.avatar+"-avatar"
        return "<img src='%s'/>" % img


@app.template_filter('savatar')
def savatar(user):
    if user.avatar == "gravatar":
        img =  Gravatar(user.email, secure=False, size=20, rating='x').thumb
        return "<img src='%s'/>" % img
    elif user.avatar == "":
        img =  app.config['AVATAR']
        return "<img src='%s'/>" % img 
    else:
        img = app.config['QINIU_URL']+user.avatar+"-savatar"
        return "<img src='%s'/>" % img 


        
@app.template_filter('timesince')
def timesince(value):
    now = datetime.datetime.utcnow()
    delta = now - value
    if delta.days > 365:
        num = delta.days/365
        return u'%s年前'% num
    if delta.days > 30:
        num = delta.days/30
        return u'%s个月前'% num
    if delta.days > 0:
        num = delta.days
        return u'%s天前'% num
    if delta.seconds > 3600:
        num = delta.seconds/3600
        return u'%s小时前'% num
    if delta.seconds > 60:
        num = delta.seconds/60
        return u'%s分钟前'% num
    return u'刚刚'

@app.template_filter('time')
def datatime(v):
    time = v.strftime('%Y-%m-%d %H:%M:%S')
    return time

@app.template_filter('timefeed')
def datatimefeed(v):
    time = v.strftime('%Y-%m-%dT%H:%M:%SZ')
    return time



@app.template_filter('content')
def content(v):
    lines = v.split('\r\n');
    c = list()
    for l in lines:
        c.append(escape(l));
        c.append(' <br/> ')
    content = "".join(c)
    content = sinaimg(content)
    content = youku(content)
    content = tudou(content)
    content = mentions(content)
    content = autolink(content)

    return content

def sinaimg(value):
    imgs = re.findall('(http://ww[0-9]{1}.sinaimg.cn/[a-zA-Z0-9]+/[a-zA-Z0-9]+.[a-z]{3})\s?', value)
    for img in imgs:
        value = value.replace(img, '<a href="' + img + '" target="_blank"><img src="' + img + '" class="imgly" border="0" /></a>')
    baidu_imgs = re.findall('(http://(bcs.duapp.com|img.xiachufang.com|i.xiachufang.com)/([a-zA-Z0-9\.\-\_\/]+).jpg)\s?', value)
    for img in baidu_imgs:
        value = value.replace(img[0], '<a href="' + img[0] + '" target="_blank"><img src="' + img[0] + '" class="imgly" border="0" /></a>')
    return value

def youku(value):
    videos = re.findall('(http://v.youku.com/v_show/id_[a-zA-Z0-9\=]+.html)\s?', value)
    if (len(videos) > 0):
        for video in videos:
            video_id = re.findall('http://v.youku.com/v_show/id_([a-zA-Z0-9\=]+).html', video)
            value = value.replace('http://v.youku.com/v_show/id_' + video_id[0] + '.html', '<embed src="http://player.youku.com/player.php/sid/' + video_id[0] + '/v.swf" quality="high" width="638" height="420" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash"></embed>')
        return value
    else:
        return value

def tudou(value):
    videos = re.findall('(http://www.tudou.com/programs/view/[a-zA-Z0-9\=]+/)\s?', value)
    if (len(videos) > 0):
        for video in videos:
            video_id = re.findall('http://www.tudou.com/programs/view/([a-zA-Z0-9\=]+)/', video)
            value = value.replace('http://www.tudou.com/programs/view/' + video_id[0] + '/', '<embed src="http://www.tudou.com/v/' + video_id[0] + '/" quality="high" width="638" height="420" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash"></embed>')
        return value
    else:
        return value

def mentions(value):
    ms = re.findall(ur'(@[a-zA-Z0-9\_\u4e00-\u9fa5]+\.?)\s?', value)
    print ms
    if (len(ms) > 0):
        for m in ms:
            m_id = re.findall(ur'@([a-zA-Z0-9\_\u4e00-\u9fa5]+\.?)', m)
            if (len(m_id) > 0):
                if (m_id[0].endswith('.') != True):
                    value = value.replace('@' + m_id[0], '@<a href="/m/' + m_id[0] + '">' + m_id[0] + '</a>')
        return value
    else:
        return value

def autolink(text, trim_url_limit=None, nofollow=False):
    """
    Converts any URLs in text into clickable links. Works on http://, https:// and
    www. links. Links can have trailing punctuation (periods, commas, close-parens)
    and leading punctuation (opening parens) and it'll still do the right thing.

    If trim_url_limit is not None, the URLs in link text will be limited to
    trim_url_limit characters.

    If nofollow is True, the URLs in link text will get a rel="nofollow" attribute.
    """

    LEADING_PUNCTUATION  = ['(', '<', '&lt;']
    TRAILING_PUNCTUATION = ['.', ',', ')', '>', '\n', '&gt;']

    # list of possible strings used for bullets in bulleted lists
    DOTS = ['&middot;', '*', '\xe2\x80\xa2', '&#149;', '&bull;', '&#8226;']

    unencoded_ampersands_re = re.compile(r'&(?!(\w+|#\d+);)')
    word_split_re = re.compile(r'(\s+)')
    punctuation_re = re.compile('^(?P<lead>(?:%s)*)(?P<middle>.*?)(?P<trail>(?:%s)*)$' % \
        ('|'.join([re.escape(x) for x in LEADING_PUNCTUATION]),
        '|'.join([re.escape(x) for x in TRAILING_PUNCTUATION])))
    simple_email_re = re.compile(r'^\S+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+$')
    link_target_attribute_re = re.compile(r'(<a [^>]*?)target=[^\s>]+')
    html_gunk_re = re.compile(r'(?:<br clear="all">|<i><\/i>|<b><\/b>|<em><\/em>|<strong><\/strong>|<\/?smallcaps>|<\/?uppercase>)', re.IGNORECASE)
    hard_coded_bullets_re = re.compile(r'((?:<p>(?:%s).*?[a-zA-Z].*?</p>\s*)+)' % '|'.join([re.escape(x) for x in DOTS]), re.DOTALL)
    trailing_empty_content_re = re.compile(r'(?:<p>(?:&nbsp;|\s|<br \/>)*?</p>\s*)+\Z')

    trim_url = lambda x, limit=trim_url_limit: limit is not None and (x[:limit] + (len(x) >=limit and '...' or ''))  or x
    words = word_split_re.split(text)
    nofollow_attr = nofollow and ' rel="nofollow"' or ''
    for i, word in enumerate(words):
        match = punctuation_re.match(word)
        if match:
            lead, middle, trail = match.groups()
            if middle.startswith('www.') or ('@' not in middle and not middle.startswith('http://') and not middle.startswith('https://') and \
                    len(middle) > 0 and middle[0] in string.letters + string.digits and \
                    (middle.endswith('.org') or middle.endswith('.net') or middle.endswith('.com'))):
                middle = '<a href="http://%s"%s target="_blank">%s</a>' % (middle, nofollow_attr, trim_url(middle))
            if middle.startswith('http://') or middle.startswith('https://'):
                middle = '<a href="%s"%s target="_blank">%s</a>' % (middle, nofollow_attr, trim_url(middle))
            if '@' in middle and not middle.startswith('www.') and not ':' in middle \
                and simple_email_re.match(middle):
                middle = '<a href="mailto:%s">%s</a>' % (middle, middle)
            if lead + middle + trail != word:
                words[i] = lead + middle + trail
    return ''.join(words)

