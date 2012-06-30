from flask.ext.wtf import (Form, TextAreaField, TextField, DateTimeField,
                           validators)
from .models import Event, EventStory


class EventForm(Form):
    name = TextField('Title', validators=[validators.Required()],
                      description="Title for an event is neccessary thing")
    description = TextAreaField('Description',
                    validators=[validators.Required()],
                    description="Here should come some interesting facts about your event")

    starts_at = DateTimeField('Starts at (DD.MM.YYYY HH:MM)', validators=[validators.Required()],
                              description="DD.MM.YYYY HH:MM")
    ends_at = DateTimeField('Ends at (DD.MM.YYYY HH:MM)', validators=[validators.Required()],
                            description="DD.MM.YYYY HH:MM")
    reg_starts = DateTimeField('Registration starts at (DD.MM.YYYY HH:MM)',
                                        validators=[validators.Required()],
                                        description="DD.MM.YYYY HH:MM")
    reg_ends = DateTimeField('Registration ends at (DD.MM.YYYY HH:MM)',
                                        validators=[validators.Required()],
                                        description="DD.MM.YYYY HH:MM")

    def save(self, commit=True):
        ev = Event()
        self.populate_obj(ev)
        return commit and ev.save() or ev


class EventStoryForm(Form):
    name = TextField('Give a name for your event')
    description = TextAreaField('Place a couple of words to describe')

    def save(self, commit=True):
        ev_story = EventStory()
        self.populate_obj(ev_story)
        return commit and ev_story.save() or ev_story
