import http
from repertoire.api import api
from repertoire.api.models import ErrorResponseModel
from repertoire.common.types import Constants
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest


def _error_factory(message, error):
    """
    Package the error info in the proper format for the marshalling function
    :param message:
    :param error:
    :return: ErrorResponseModel
    """
    return {
        'message': message,
        'error': error
    }


@api.errorhandler
@api.response(http.HTTPStatus.INTERNAL_SERVER_ERROR, description=Constants.ERROR_UNHANDLED)
@api.marshal_with(ErrorResponseModel)
def default_error_handler(e):
    return _error_factory(Constants.ERROR_UNHANDLED, e), http.HTTPStatus.INTERNAL_SERVER_ERROR


@api.errorhandler(BadRequest)
@api.response(http.HTTPStatus.BAD_REQUEST, description=Constants.ERROR_BAD_REQUEST)
@api.marshal_with(ErrorResponseModel)
def bad_request_handler(e):
    return _error_factory(Constants.ERROR_BAD_REQUEST, e), http.HTTPStatus.BAD_REQUEST


@api.errorhandler(NoResultFound)
@api.response(http.HTTPStatus.NOT_FOUND, description=Constants.ERROR_DB_RESULT_NOT_FOUND)
@api.marshal_with(ErrorResponseModel)
def database_not_found_error_handler(e):
    return _error_factory(Constants.ERROR_DB_RESULT_NOT_FOUND, e), http.HTTPStatus.NOT_FOUND
