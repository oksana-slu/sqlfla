from eventor import db
from core.models import SlugMixin, CRUDMixin


__all__ = ['Event']


class EventStory(db.Model, CRUDMixin):
    # authors = db.relationship()
    name = db.Column(db.Unicode(255), nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)


class Event(db.Model, SlugMixin):
    description = db.Column(db.UnicodeText)
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    reg_starts = db.Column(db.DateTime)
    reg_ends = db.Column(db.DateTime)

    story_id = db.Column(db.Integer, db.ForeignKey('event_stories.id'))
    storyline = db.relationship('EventStory', lazy='dynamic', backref='events')
