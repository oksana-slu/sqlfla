from flask import render_template, request, redirect, url_for

from . import events
from .forms import EventForm, EventStoryForm
from .models import Event, EventStory


@events.route('/stories')
def list_stories():
    return render_template("events/list_stories.html")


@events.route('/stories/create', methods=['GET', 'POST'])
def create_story():
    story_form = EventStoryForm(request.form or None)

    if request.form and story_form.validate():
        story_form.save()
        return redirect(url_for('.list_stories'))

    return render_template('events/create_story.html', story_form=story_form)


@events.route('/stories/<int:id>/create', methods=['GET', 'POST'])
def create_event(id):
    story = EventStory.query.get_or_404(id)
    form = EventForm(request.form or None)

    if request.form and form.validate():
        ev = form.save(commit=False)
        ev.storyline = story
        ev.save()
        return redirect(url_for('.show_event', id=ev.id))

    return render_template("events/create.html", event_form=form)


@events.route('/<int:id>')
def show_event(id):
    return render_template("events/show.html", event=Event.get_or_404(id))
