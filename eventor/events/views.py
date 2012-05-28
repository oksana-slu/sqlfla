from flask import render_template, request

from . import events
from .forms import EventForm


@events.route('/')
def list():
    return render_template("events/list.html")


@events.route('/create', methods=['GET', 'POST'])
def create():
    form = EventForm(request.form or None)
    return render_template("events/create.html", event_form=form)
