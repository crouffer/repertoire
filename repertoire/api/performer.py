from flask_restplus import Resource
from repertoire.api import api
from repertoire.common.repertoire_ioc import RepertoireIOC as ri
from repertoire.common.types import Constants

import http

ns = api.namespace(Constants.NS_PERFORMER, description='Performer Information')
dal = ri.get_dal()


@ns.route('/')
class PersonList(Resource):

    from repertoire.api.models import PersonModel

    @api.response(http.HTTPStatus.OK, Constants.STATUS_OK)
    @api.marshal_with(PersonModel, as_list=True)
    def get(self):
        """
        Return a list of all performers
        """
        person_list = dal.get_person_list(offset=None, limit=None)

        return person_list
