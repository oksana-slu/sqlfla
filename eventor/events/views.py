from flask import abort, g, render_template, request, redirect, url_for

from . import events
from .forms import EventForm, EventStoryForm
from .models import Event, EventStory


@events.route('/stories')
def list_stories():
    return render_template("events/list_stories.html", stories=g.user.stories)


@events.route('/stories/create', methods=['GET', 'POST'])
def create_story():
    story_form = EventStoryForm(request.form or None)

    if request.form and story_form.validate():
        story_form.save()
        return redirect(url_for('.list_stories'))

    return render_template('events/create_story.html', story_form=story_form)


@events.route('/stories/<int:id>')
def show_story(id):
    story = EventStory.query.get_or_404(id)
    story.author.first() == g.user or abort(403)
    return render_template('events/show_story.html',
                    story=story)


@events.route('/stories/<int:id>/edit', methods=['GET', 'POST'])
def edit_story(id):
    story = EventStory.query.get_or_404(id)
    story_form = EventStoryForm(request.form or None, obj=story)

    if request.form and story_form.validate():
        story_form.save(story)
        return redirect(url_for('.show_story', id=story.id))

    return render_template('events/edit_story.html', story_form=story_form,
                           story=story)


@events.route('/stories/<int:id>/delete')
def remove_story(id):
    story = EventStory.query.get_or_404(id)
    story.author.first() == g.user or abort(403)
    story.delete()
    return redirect(url_for('.list_stories'))


@events.route('/stories/<int:id>/create', methods=['GET', 'POST'])
def create_event(id):
    story = EventStory.query.get_or_404(id)
    form = EventForm(request.form or None)
    print request.form
    if request.form and form.validate():
        ev = form.save()
        story.events.append(ev)
        ev.save()
        return redirect(url_for('.show_event', id=ev.id))

    return render_template("events/create.html", story=story,
                           event_form=form)


@events.route('/<int:id>')
def show_event(id):
    return render_template("events/show.html", event=Event.get_or_404(id))
