from repertoire.api.healthcheck import HealthCheck
from repertoire.common.types import Constants


def test_health_check_response():

    uut = HealthCheck()

    response = uut.get()
    assert 'status' in response
    assert response['status'] == Constants.STATUS_OK
    assert 'timestamp' in response

    # Convert the string back to a date, and make sure it makes sense
    from datetime import datetime
    date_obj = datetime.strptime(response['timestamp'], Constants.FORMAT_ISO_8601_DATETIME)
    assert date_obj is not None
    assert date_obj <= datetime.utcnow()
