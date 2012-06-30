# -*- encoding: utf-8 -*-
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr

from eventor import db
from core.models import SlugMixin, CRUDMixin


__all__ = ['Event']


class EventStory(db.Model, CRUDMixin):
    # authors = db.relationship()
    name = db.Column(db.Unicode(255), nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)


class EventParticipant(db.Model, CRUDMixin):

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('Event', backref='event_participants')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', lazy='dynamic', backref='participating')

    descriminator = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_on': descriminator,
        'polymorphic_identity': 'participant'
    }


class ParticipantMixin(EventParticipant):
    __abstract__ = True

    @declared_attr
    def id(cls):
        return db.Column(db.Integer, db.ForeignKey('event_participants.id'), primary_key=True)


class EventManager(ParticipantMixin):
    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }
    # event = db.relationship('Event', backref='event_managers')
    event = db.relationship('Event', backref='event_managers')
    user = db.relationship('User', lazy='dynamic', backref='managing')


class EventSpeaker(ParticipantMixin):
    __mapper_args__ = {
        'polymorphic_identity': 'speaker'
    }
    event = db.relationship('Event', backref='event_speakers')
    user = db.relationship('User', lazy='dynamic', backref='speaking')


class Event(db.Model, SlugMixin):
    description = db.Column(db.UnicodeText)
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    reg_starts = db.Column(db.DateTime)
    reg_ends = db.Column(db.DateTime)

    story_id = db.Column(db.Integer, db.ForeignKey('event_stories.id'))
    storyline = db.relationship('EventStory', lazy='dynamic', backref='events')

    participants = association_proxy('event_participants', 'user')
    managers = association_proxy('event_managers', 'user')
    speakers = association_proxy('event_speakers', 'user')
