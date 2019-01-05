from flask_restplus import fields
from repertoire.api.restplus import api

HealthCheckStatusModel = api.model('HealthCheckStatusModel', {
    'status': fields.String(),
    'timestamp': fields.DateTime()
})
