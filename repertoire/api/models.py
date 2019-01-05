from flask_restplus import fields
from repertoire.api import api

ErrorResponseModel = api.model('ErrorResponseModel', {
    'message': fields.String(),
    'error': fields.String()
})

HealthCheckStatusModel = api.model('HealthCheckStatusModel', {
    'status': fields.String(),
    'timestamp': fields.DateTime()
})
