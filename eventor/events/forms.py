from flask.ext.wtf import (Form, TextAreaField, TextField, DateTimeField,
                           validators)
from .models import Event


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
