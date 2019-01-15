# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.auth_controller import api as auth_ns
from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Flask Restplus API Boilerplate With JWT',
          version='1.0',
          description='boilerplate for a flask restplus web service'
          )

api.add_namespace(auth_ns)
api.add_namespace(user_ns, path='/user')
