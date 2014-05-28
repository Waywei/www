import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

bind = '127.0.0.1:5000'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'egg:gunicorn#gevent'

# you should change this
user = 'root'

# maybe you like error
#accesslog = '-'
#loglevel = 'warning'
#errorlog = '-'

secure_scheme_headers = {
    'X-SCHEME': 'https',
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on',
}
x_forwarded_for_header = 'X-FORWARDED-FOR'
