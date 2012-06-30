from flask import render_template, request, redirect, url_for

from . import events
from .forms import EventForm
from .models import Event


@events.route('/')
def list():
    return render_template("events/list.html")


@events.route('/create', methods=['GET', 'POST'])
def create():
    form = EventForm(request.form or None)
    if form.validate():
        ev = form.save()
        return redirect(url_for('events.show', id=ev.id))
    return render_template("events/create.html", event_form=form)


@events.route('/show/<int:id>')
def show(id):
    return render_template("events/show.html", event=Event.get_or_404(id))
