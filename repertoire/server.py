# /server.py

from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.flask.client import OAuth

app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='1YouO3UUvFu8Tp9FEra0EBwbS7Q8Gial',
    client_secret='YOUR_CLIENT_SECRET',
    api_base_url='https://crouffer.auth0.com',
    access_token_url='https://crouffer.auth0.com/oauth/token',
    authorize_url='https://crouffer.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


