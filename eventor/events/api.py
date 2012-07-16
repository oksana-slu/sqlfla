from flask import request

from eventor.core.resources import ModelResource
from eventor.core.decorators import api_resource

from eventor.auth.models import User
from . import events
from .models import event_participants


@api_resource(events, 'participants', {'id': int})
class Participants(ModelResource):

    model = User

    include = ['first_name', 'last_name', 'email', 'active', 'phone']

    def get_objects(self):
        args = request.args.to_dict()
        if 'event' in args:
            participant_type = args.get('p_type', 0)

            return User.query.join(event_participants)\
                    .filter(event_participants.c.event_id == args['event'],
                            event_participants.c.p_type == participant_type)
                # if 'event' in args:
        else:
            return super(Participants, self).get_objects().filter_by(id=-1)
