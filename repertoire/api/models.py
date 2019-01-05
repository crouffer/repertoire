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


PersonModel = api.model('PersonModel', {
    'id': fields.Integer(),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'date_added': fields.DateTime(required=False)
})
