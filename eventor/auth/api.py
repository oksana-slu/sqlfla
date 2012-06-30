from eventor.core.decorators import api_resource
from eventor.core.resources import ModelResource
from eventor.auth.models import User
from . import auth


@api_resource(auth, 'sessions', {'id': None})
class SessionResource(ModelResource):
    model = User
