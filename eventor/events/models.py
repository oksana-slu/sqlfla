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

events_managers = db.Table('events_managers', db.metadata,
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'),
              primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'),
              primary_key=True),
)

events_participants = db.Table('events_participants', db.metadata,
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'),
              primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'),
              primary_key=True),
)


class Event(db.Model, SlugMixin):
    description = db.Column(db.UnicodeText)
    starts_at = db.Column(db.DateTime, nullable=False)
    ends_at = db.Column(db.DateTime, nullable=False)
    reg_starts = db.Column(db.DateTime, nullable=False)
    reg_ends = db.Column(db.DateTime, nullable=False)

    story_id = db.Column(db.Integer, db.ForeignKey('event_stories.id'))
    storyline = db.relationship('EventStory', lazy='dynamic', backref='events')

    participants = db.relationship('User', secondary=events_participants,
                                   backref='participant_for')
    managers = db.relationship('User', secondary=events_managers,
                                   backref='manager_for')
