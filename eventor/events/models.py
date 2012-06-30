from eventor import db
from core.models import SlugMixin, CRUDMixin


__all__ = ['Event']


class EventLine(db.Model, CRUDMixin):
    name = db.Column(db.Unicode(255))
    description = db.Column(db.UnicodeText)


class Event(db.Model, SlugMixin):
    description = db.Column(db.UnicodeText)
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    reg_starts = db.Column(db.DateTime)
    reg_ends = db.Column(db.DateTime)

    story_id = db.Column(db.Integer, db.ForeignKey('event_lines.id'))
    storyline = db.relationship('EventLine', lazy='dynamic', backref='events')
