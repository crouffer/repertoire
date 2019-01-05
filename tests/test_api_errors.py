import http

from repertoire.common.types import Constants

from faker import Faker
fake = Faker()


class TestApiErrors(object):

    def test_no_database_result_found_response(self):
        from repertoire.api.errors import database_not_found_error_handler

        error_string = fake.text()
        response = database_not_found_error_handler(error_string)
        assert response is not None
        assert response[0]['message'] == Constants.ERROR_DB_RESULT_NOT_FOUND
        assert response[0]['error'] == error_string
        assert response[1] == http.HTTPStatus.NOT_FOUND

    def test_bad_request_handler_response(self):
        from repertoire.api.errors import bad_request_handler

        error_string = fake.text()
        response = bad_request_handler(error_string)
        assert response is not None
        assert response[0]['message'] == Constants.ERROR_BAD_REQUEST
        assert response[0]['error'] == error_string
        assert response[1] == http.HTTPStatus.BAD_REQUEST

    def test_default_error_handler_response(self):
        from repertoire.api.errors import default_error_handler

        error_string = fake.text()
        response = default_error_handler(error_string)
        assert response is not None
        assert response[0]['message'] == Constants.ERROR_UNHANDLED
        assert response[0]['error'] == error_string
        assert response[1] == http.HTTPStatus.INTERNAL_SERVER_ERROR
