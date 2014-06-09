import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SECRET_KEY = 'www.bearwave.com'
PASSWORD_SECRET = 'www.bearwave.com'

#SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:password@localhost:3306/test?charset=utf8'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'test.db')
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/bearwave'
DATABASE_CONNECT_OPTIONS = {}

SESSION_COOKIE_NAME = 'bearwave'
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30

SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCEL = 3600

#CSRF_ENABLED=True
#CSRF_SESSION_KEY="somethingimpossibletoguess"

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LegmvMSAAAAAIgqBAH_SVf4S3KynoD3qrdd4IWW'
RECAPTCHA_PRIVATE_KEY = '6LegmvMSAAAAAAIZPRf8R7DRc5oufSmpYx9HDsQW'
RECAPTCHA_OPTIONS = {'theme': 'white'}

BASEURL = 'http://www.bearwave.com/'
SURL = 'http://s.bearwave.com/'
BASETITLE = 'bearwave'
EMAIL = "syllor@bearwave.com"

DEV = True

MAILGUN = ''
