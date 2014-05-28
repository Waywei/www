from db import db
from models import User
from cherrymoon import app

from flask.ext.restless import APIManager
manager = APIManager(app, flask_sqlalchemy_db=db)


manager.create_api(User,
    methods=['GET'],
    preprocessors = {
        'GET_SINGLE':[get_single],
                
    },
    postprocessors = {
        ''    
    }
) 

