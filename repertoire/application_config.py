# Flask settings
FLASK_SERVER_ADDRESS = '0.0.0.0'
FLASK_SERVER_PORT = 5000
FLASK_SERVER_NAME = '{0}:{1}'.format(FLASK_SERVER_ADDRESS, FLASK_SERVER_PORT)
FLASK_DEBUG = False  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = True

# SQLAlchemy settings
import os
DB_ADDRESS = os.environ.get('DB_ADDRESS')
DB_NAME = os.environ.get('DB_NAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

DB_ENGINE = 'mssql'
if DB_ENGINE == 'mssql':    #pragma: no cover
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://{}:{}@{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_ADDRESS, DB_NAME)
elif DB_ENGINE == 'mysql':  #pragma: no cover
    SQLALCHEMY_DATABASE_URI = 'mysql+pymssql://{}:{}@{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_ADDRESS, DB_NAME)
elif DB_ENGINE == 'sqlite': #pragma: no cover
    SQLALCHEMY_DATABASE_URI = 'sqlite://{}:{}@{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_ADDRESS, DB_NAME)
else:   #pragma: no cover
    raise RuntimeError("Unsupported DB_ENGINE: {}".format(DB_ENGINE))


SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_MAX_OVERFLOW = 40
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# URL Prefix for API routes
URL_PREFIX = '/api'

# File Upload location
UPLOAD_FOLDER = '/tmp'

# Mandatory Environment Variables
MANDATORY_ENVIRONMENT_VARS = []
