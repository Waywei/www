from flask import flash,render_template, redirect,url_for
from flask import g, request, flash, session
from cherrymoon import app
from cherrymoon.ext.db import db
from cherrymoon.models import Interview,Topic,Node,Comment,User
from cherrymoon.models import Page, Looking
from cherrymoon.ext.helper import is_admin
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from wtforms import TextAreaField
from wtforms.widgets import TextArea

admin = Admin(app,name="cherrymoon")
class MyView(ModelView):
    def is_accessible(self):
        return is_admin()

class LoginView(BaseView):
    @expose('/index/')
    def index(self):
        return self.render('index.html')

class FileCheckAdmin(FileAdmin):
    def is_accessible(self):
        return is_admin()

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)
 
class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class RichEditorView(ModelView):
    def is_accessible(self):
        return is_admin()

    form_overrides = dict(text=CKTextAreaField)
    create_template = '/admin/edit.html'
    edit_template = '/admin/edit.html'
 

admin.add_view(RichEditorView(Page,db.session))
admin.add_view(RichEditorView(Interview,db.session))
admin.add_view(MyView(Topic,db.session))
admin.add_view(MyView(Node,db.session))
admin.add_view(MyView(Comment,db.session))
admin.add_view(MyView(User,db.session))
admin.add_view(MyView(Looking,db.session))

import os.path as op

#path = op.join(op.dirname(__file__), 'public/static')
#admin.add_view(FileCheckAdmin(path, '/static/', name='Static Files'))


