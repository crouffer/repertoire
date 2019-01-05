# import traceback
#
from flask import current_app as app
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest

api = Api(
    version='0.1',
    title='Repertoire Song Catalogue',
    description='API For the Repertoire Song Catalogue',
    catch_all_404s=True,
    default_mediatype='application/json'
    )


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    app.logger.exception(message)
    return {'message': message}, 500


@api.errorhandler(BadRequest)
def bad_request_handler(e):
    app.logger.exception(e)
    return {'error': e}, 400


# @api.errorhandler(NoResultFound)
# def database_not_found_error_handler(e):
#     app.logger.warning(traceback.format_exc())
#     return {'message': 'A database result was required but none was found.'}, 404
