from flask.ext.wtf import (Form, TextAreaField, TextField, DateTimeField,
                           validators)


class EventForm(Form):
    title = TextField('Title', validators=[validators.Required()],
                      description="Title for an event is neccessary thing")
    description = TextAreaField('Description',
                    validators=[validators.Required()],
                    description="Here should come some interesting facts about your event")

    starts_at = DateTimeField('Starts at (MM.DD.YYYY HH:MM)', validators=[validators.Required()],
                              description="MM.DD.YYYY HH:MM")
    ends_at = DateTimeField('Ends at (MM.DD.YYYY HH:MM)', validators=[validators.Required()],
                            description="MM.DD.YYYY HH:MM")
    registration_starts = DateTimeField('Registration starts at (MM.DD.YYYY HH:MM)',
                                        validators=[validators.Required()],
                                        description="MM.DD.YYYY HH:MM")
    registration_ends = DateTimeField('Registration ends at (MM.DD.YYYY HH:MM)',
                                        validators=[validators.Required()],
                                        description="MM.DD.YYYY HH:MM")
