class Constants:
    """
    All constants for the repertoire app, listed in alphabetical order
    """
    AUTH0_CLIENT_ID = 'AUTH0_CLIENT_ID'
    AUTH0_CLIENT_SECRET = 'AUTH0_CLIENT_SECRET'
    AUTH0_CALLBACK_URL = 'AUTH0_CALLBACK_URL'
    AUTH0_DOMAIN = 'AUTH0_DOMAIN'
    AUTH0_AUDIENCE = 'AUTH0_AUDIENCE'
    PROFILE_KEY = 'profile'
    SECRET_KEY = 'ThisIsTheSecretKey'
    JWT_PAYLOAD = 'jwt_payload'

    # Error messages
    ERROR_BAD_REQUEST = 'Bad request'
    ERROR_DB_RESULT_NOT_FOUND = 'A database result was required but none was found'
    ERROR_UNHANDLED = 'An unhandled exception occurred'

    # String formats
    FORMAT_DATE = '%Y-%m-%d'
    FORMAT_ISO_8601_DATETIME = '%Y-%m-%dT%H:%M:%S.%f'
    FORMAT_TIME = '%H:%M:%S %Z'

    # Namespaces
    NS_HEALTH_CHECK = 'health_check'

    # Status codes
    STATUS_OK = 'ok'


