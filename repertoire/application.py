import logging


class RequestIdFilter(logging.Filter):  # pragma: no cover
    """Enhances log messages with request_id information"""

    def filter(self, record):
        from flask import request
        try:
            request_id = request.headers['request_id']
            record.request_id = request_id
        except Exception as e:
            if str(e).startswith('Working outside of request context'):
                record.request_id = 'not-in-request-context'
            else:
                record.request_id = 'request-id-not-set'
        return True


class Application:

    DEFAULT_CONFIG_FILE_NAME = 'application_config.py'

    """
    Application main class
    """
    @classmethod
    def __init__(cls, gunicorn=False):
        """
        Create and initialize the Flask application
        """
        # In gunicorn the logging is handled differently
        cls._gunicorn=gunicorn

        from flask import Flask
        cls.app = Flask(__name__)
        cls._initialize_app()
        cls._initialize_authentication()
        cls._initialize_logger()
        cls._initialize_routes()
        cls.app.logger.info('Application initialized')

    @classmethod
    def _initialize_app(cls, config_file=DEFAULT_CONFIG_FILE_NAME):
        cls.app.config.from_pyfile(config_file)
        cls._validate_environment()

        # Without this, swagger.json is served using HTTP, not HTTPS
        # See https://github.com/noirbizarre/flask-restplus/issues/54
        from werkzeug.contrib.fixers import ProxyFix
        cls.app.wsgi_app = ProxyFix(cls.app.wsgi_app)

    @classmethod
    def _initialize_api_routes(cls):
        from .api.healthcheck import ns as health_check_namespace
        from .api import api

        from flask import Blueprint
        blueprint = Blueprint('api', __name__, url_prefix=cls.app.config['URL_PREFIX'])
        api.init_app(blueprint)
        api.add_namespace(health_check_namespace)
        cls.app.register_blueprint(blueprint)

    @classmethod
    def _initialize_authentication(cls):
        from authlib.flask.client import OAuth

        oauth = OAuth(cls.app)

        cls.auth0 = oauth.register(
            'auth0',
            client_id=cls.app.config['AUTH0_CLIENT_ID'],
            client_secret=cls.app.config['AUTH0_CLIENT_SECRET'],
            api_base_url=cls.app.config['AUTH0_API_BASE_URL'],
            access_token_url=cls.app.config['AUTH0_ACCESS_TOKEN_URL'],
            authorize_url=cls.app.config['AUTH0_AUTHORIZE_URL'],
            client_kwargs={
                'scope': 'openid profile',
            },
        )

    @classmethod
    def _initialize_database(cls):  # pragma: no cover
        # Initialize the database

        # Close sessions when leaving app context
        @cls.app.teardown_appcontext
        def shutdown_session(exception=None):
            # from database.flask_db import get_db
            # db = get_db()
            # db.session.close_all()
            # db.session.remove()
            pass

    @classmethod
    def _initialize_logger(cls):
        import logging

        # Format the logs with the request_id and other useful information
        log_format = '%(levelname)s - Request-Id: %(request_id)s - %(asctime)s [%(filename)s:%(lineno)d]: %(message)s'
        log_formatter = logging.Formatter(log_format)

        if cls._gunicorn:   # pragma: no cover
            # Initialize logging from the gunicorn settings
            gunicorn_logger = logging.getLogger('gunicorn.error')
            cls.app.logger.handlers = gunicorn_logger.handlers
            cls.app.logger.setLevel(gunicorn_logger.level)
        else:
            # Default logging level when running as a flask-dev server app
            cls.app.logger.setLevel(logging.DEBUG)

        for log_handler in cls.app.logger.handlers:     # pragma: no cover
            log_handler.setFormatter(log_formatter)
            log_handler.addFilter(RequestIdFilter())

    @classmethod
    def _initialize_routes(cls):
        cls._initialize_api_routes()
        cls._initialize_static_routes()

        from flask_cors import CORS
        CORS(cls.app)

    @classmethod
    def _initialize_static_routes(cls):
        import http

        @cls.app.route('/callback')
        def callback_handling():
            # Handles response from token endpoint
            cls.auth0.authorize_access_token()
            resp = cls.auth0.get('userinfo')
            userinfo = resp.json()

            # Store the user information in flask session.
            from flask import redirect,     session
            session['jwt_payload'] = userinfo
            session['profile'] = {
                'user_id': userinfo['sub'],
                'name': userinfo['name'],
                'picture': userinfo['picture']
            }
            return redirect('/dashboard')

        @cls.app.route('/login')
        def login():
            return cls.auth0.authorize_redirect(redirect_uri=cls.app.config['AUTH0_CALLBACK_URL'],
                                                audience=cls.app.config['AUTH0_AUDIENCE'])

        def requires_auth(f):
            from functools import wraps

            @wraps(f)
            def decorated(*args, **kwargs):
                from flask import redirect, session
                if 'profile' not in session:
                    # Redirect to Login page here
                    return redirect('/')
                return f(*args, **kwargs)

                return decorated

        @cls.app.route('/dashboard')
        @requires_auth
        def dashboard():
            from flask import render_template, session
            import json
            return render_template('dashboard.html',
                                   userinfo=session['profile'],
                                   userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

        @cls.app.route('/logout')
        def logout():
            from flask import redirect, session, url_for
            from six.moves.urllib.parse import urlencode
            # Clear session stored data
            session.clear()
            # Redirect user to logout endpoint
            params = {'returnTo': url_for('home', _external=True), 'client_id': cls.app.config['AUTH0_CLIENT_ID']}
            return redirect(cls.auth0.api_base_url + '/v2/logout?' + urlencode(params))

        @cls.app.route('/')
        def route_base_url():   # pragma: no cover
            from flask import redirect, url_for
            path = 'api.doc'
            new_url = url_for(path)
            return redirect(new_url)

        @cls.app.route('/api/swagger')
        def gen_swagger():   # pragma: no cover
            from flask import json
            from repertoire.api import api
            data = json.dumps(api.__schema__, indent=2)

            return data, http.HTTPStatus.OK

        @cls.app.route('/api/config')
        def get_s3_config():   # pragma: no cover
            import json
            data = {
                'DB_ADDRESS': cls.app.config['DB_ADDRESS']
            }
            return json.dumps(data), http.HTTPStatus.OK

        @cls.app.route('/shutdown', methods=['POST'])
        def shutdown():   # pragma: no cover
            cls._shutdown_server()
            return 'Server shutting down...'

    @classmethod
    def _shutdown_server(cls):   # pragma: no cover
        from flask import request
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @classmethod
    def _validate_environment(cls):     # pragma: no cover
        try:
            mandatory_env_vars = cls.app.config['MANDATORY_ENVIRONMENT_VARS']
        except KeyError:    # pragma: no cover
            # No mandatory environment vars specified
            mandatory_env_vars = []

        error_detected = False
        for v in mandatory_env_vars:
            cls.is_env_var_set(v)

        if error_detected:
            raise RuntimeError("Initialization failed.  Missing mandatory environment variable(s)")

    @classmethod
    def get_app(cls):
        """
        Get the initialized application object
        :return:
        """
        return cls.app

    @classmethod
    def is_env_var_set(cls, varname):   # pragma: no cover
        import os
        if not os.getenv(varname, False):
            cls.app.logger.info("Environment variable {} is not set".format(varname))
            return False
        else:
            return True


def create_app():
    return Application().get_app()


def start_dev_server(app):   # pragma: no cover
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False, threaded=True)
