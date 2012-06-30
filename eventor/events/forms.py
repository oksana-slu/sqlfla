from flask import g
from flask.ext.wtf import (Form, TextAreaField, TextField, DateTimeField,
                           validators)
from .models import Event, EventStory


class EventForm(Form):
    name = TextField('Title', validators=[validators.Required()],
                      description="Title for an event is neccessary thing")
    description = TextAreaField('Description',
                    validators=[validators.Required()],
                    description="Here should come some interesting facts about your event")

    starts_at = DateTimeField('Starts at (DD.MM.YYYY HH:MM)',
                              format='%d.%m.%Y %H:%M',
                              validators=[validators.Required()],
                              description="DD.MM.YYYY HH:MM")
    ends_at = DateTimeField('Ends at (DD.MM.YYYY HH:MM)',
                            format='%d.%m.%Y %H:%M',
                            validators=[validators.Required()],
                            description="DD.MM.YYYY HH:MM")
    reg_starts = DateTimeField('Registration starts at (DD.MM.YYYY HH:MM)',
                               format='%d.%m.%Y %H:%M',
                               validators=[validators.Required()],
                               description="DD.MM.YYYY HH:MM")
    reg_ends = DateTimeField('Registration ends at (DD.MM.YYYY HH:MM)',
                             format='%d.%m.%Y %H:%M',
                             validators=[validators.Required()],
                             description="DD.MM.YYYY HH:MM")
    address = TextAreaField('Address', description="Input address details",
                            validators=[validators.Required()])
    max_participants = TextField('Participants limit',
                                 description='Max. participants')

    def save(self, obj=None, commit=True):
        ev = obj or Event()
        self.populate_obj(ev)
        g.user.manager_for.append(ev)
        return commit and ev.save() or ev


class EventStoryForm(Form):
    name = TextField('Title: *', description="Give a name to your event",
                    validators=[validators.Required()])
    description = TextAreaField('Description: *',
                    description="Place a couple of words to describe",
                    validators=[validators.Required()])

    def save(self, obj=None, commit=True):
        story = obj or EventStory()
        self.populate_obj(story)
        g.user.stories.append(story)
        return commit and story.save() or story
