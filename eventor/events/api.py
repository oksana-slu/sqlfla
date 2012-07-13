from flask import request, current_app

from eventor import db
from eventor.core.resources import ModelResource
from eventor.core.decorators import api_resource

from eventor.auth.models import User
from . import events
from .models import Event, event_participants


@api_resource(events, 'participants', {'id': int})
class Participants(ModelResource):

    model = User

    include = ['first_name', 'last_name', 'email', 'active', 'phone']

    def get_objects(self):
        args = request.args.to_dict()
        p_type = int(args['p_type']) if 'p_type' in args else  0
        if 'event' in args:
            # for user in User.query.join('participant_for').filter_by(id=args['event']):
            return User.query.join(event_participants)\
                        .filter(event_participants.c.event_id == args['event'],
                                event_participants.c.p_type == p_type)
                # if 'event' in args:
        else:
            return super(Participants, self).get_objects().filter_by(id=-1)
