# -*- encoding: utf-8 -*-
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr

from eventor import db
from core.models import SlugMixin, CRUDMixin
from core.utils import plural_name, underscorize


__all__ = ['Event']

plural_under = lambda name: plural_name(underscorize(name))
lazy_cascade = {
    'lazy': 'dynamic',
    'cascade': 'all',
}


class EventStory(db.Model, CRUDMixin):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='stories', uselist=False, **lazy_cascade)
    name = db.Column(db.Unicode(255), nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)

    @property
    def active(self):
        return Event.query.filter_by(story_id=self.id) \
            .filter(Event.reg_starts >= datetime.utcnow(),
                    Event.reg_ends <= datetime.utcnow())


class ParticipantMixin(CRUDMixin):

    @declared_attr
    def event_id(cls):
        return db.Column(db.Integer, db.ForeignKey('events.id'))

    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'))


class EventParticipant(db.Model, ParticipantMixin):
    event = db.relationship('Event', backref='event_participants', **lazy_cascade)
    user = db.relationship('User', backref='participating', **lazy_cascade)


class EventManager(db.Model, ParticipantMixin):
    event = db.relationship('Event', backref='event_managers', **lazy_cascade)
    user = db.relationship('User', backref='managing', **lazy_cascade)


class EventSpeaker(db.Model, ParticipantMixin):
    event = db.relationship('Event', backref='event_speakers', **lazy_cascade)
    user = db.relationship('User', backref='speaking', **lazy_cascade)


class Event(db.Model, SlugMixin):
    description = db.Column(db.UnicodeText)
    starts_at = db.Column(db.DateTime, nullable=False)
    ends_at = db.Column(db.DateTime, nullable=False)
    reg_starts = db.Column(db.DateTime, nullable=False)
    reg_ends = db.Column(db.DateTime, nullable=False)

    story_id = db.Column(db.Integer, db.ForeignKey('event_stories.id'))
    storyline = db.relationship('EventStory', lazy='dynamic', backref='events')

    participants = association_proxy('event_participants', 'user')
    managers = association_proxy('event_managers', 'user')
    speakers = association_proxy('event_speakers', 'user')
