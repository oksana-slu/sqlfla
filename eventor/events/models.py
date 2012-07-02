# -*- encoding: utf-8 -*-
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr

from eventor import db
# from eventor.auth.models import User

from eventor.core.models import SlugMixin, CRUDMixin
from eventor.core.utils import plural_name, underscorize


__all__ = ['Event']

plural_under = lambda name: plural_name(underscorize(name))
lazy_cascade = {
    'lazy': 'dynamic',
    'cascade': 'all',
}


class EventStory(db.Model, CRUDMixin):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('stories', **lazy_cascade), uselist=False)
    name = db.Column(db.Unicode(255), nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)

    @property
    def active(self):
        return self.events.filter(Event.reg_starts <= datetime.utcnow(),
                                  Event.reg_ends >= datetime.utcnow())

    @property
    def archive(self):
        return self.events.except_(self.active)


events_managers = db.Table('events_managers', db.metadata,
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'),
              primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'),
              primary_key=True),
)

event_participants = db.Table('events_participant', db.metadata,
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('p_type', db.Integer, default=0)
)


class Event(db.Model, SlugMixin):
    description = db.Column(db.UnicodeText)
    starts_at = db.Column(db.DateTime, nullable=False)
    ends_at = db.Column(db.DateTime, nullable=False)
    reg_starts = db.Column(db.DateTime, nullable=False)
    reg_ends = db.Column(db.DateTime, nullable=False)

    story_id = db.Column(db.Integer, db.ForeignKey('event_stories.id'))
    storyline = db.relationship('EventStory', backref=db.backref('events', **lazy_cascade))

    # participants = association_proxy('p_users', 'user',
    #                 creator=lambda u: EventsParticipant(user_id=u.id))
    participants = db.relationship('User', secondary=event_participants,
                    backref='participant_for', passive_deletes=True)
    managers = db.relationship('User', secondary=events_managers,
                    backref='manager_for', passive_deletes=True)
