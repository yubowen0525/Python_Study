import datetime

from connexion import NoContent
from flask import request
from flask.views import MethodView


class PetsView(MethodView):
    """Create Pets service"""

    method_decorators = []
    pets = {}

    def post(self):
        pass

    def put(self, petId):
        pass

    def delete(self, petId):
        id_ = int(petId)
        if self.pets.get(id_) is None:
            return NoContent, 404
        del self.pets[id_]
        return NoContent, 204

    def get(self, petId):
        id_ = int(petId)
        if self.pets.get(id_) is None:
            return NoContent, 404
        return self.pets[id_]

    def search(self, limit=100):
        # NOTE: we need to wrap it with list for Python 3 as dict_values is not JSON serializable
        return {"a": "test"}
