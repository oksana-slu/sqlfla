# -*- encoding: utf-8 -*-
import re
from flask import abort, g, render_template, request, redirect, Response, url_for
from flask.ext.security import login_required
from . import events
from eventor.events.forms import EventForm, EventStoryForm
from eventor.events.models import Event, EventStory
from eventor.core.utils import jsonify_status_code

re_container = re.compile('event(?P<id>\d+)Container')


@events.route('/stories')
@login_required
def list_stories():
    return render_template("events/list_stories.html", stories=g.user.stories)


@events.route('/stories/create', methods=['GET', 'POST'])
@login_required
def create_story():
    story_form = EventStoryForm(request.form or None)

    if request.form and story_form.validate():
        story_form.save()
        return redirect(url_for('.list_stories'))

    return render_template('events/create_story.html', story_form=story_form)


@events.route('/stories/<int:id>')
@login_required
def show_story(id):
    story = EventStory.query.get_or_404(id)
    story.author == g.user or abort(403)
    return render_template('events/show_story.html',
                    story=story)


@events.route('/stories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_story(id):
    story = EventStory.query.get_or_404(id)
    story_form = EventStoryForm(request.form or None, obj=story)

    if request.form and story_form.validate():
        story_form.save(story)
        return redirect(url_for('.show_story', id=story.id))

    return render_template('events/edit_story.html', story_form=story_form,
                           story=story)


@events.route('/stories/<int:id>/delete')
@login_required
def remove_story(id):
    story = EventStory.query.get_or_404(id)
    story.author == g.user or abort(403)
    story.delete()
    return redirect(url_for('.list_stories'))


@events.route('/stories/<int:id>/create', methods=['GET', 'POST'])
@login_required
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
@login_required
def show_event(id):
    return render_template("events/show.html", event=Event.query.get_or_404(id))


@events.route('/wdgt/')
def widget():
    c = request.args.get('c') or abort(404)
    matched = re_container.match(c) or abort(404)
    event_id = matched.groupdict()['id']
    response = Response(content_type="text/javascript")
    response.data = render_template('events/widget.js', event=Event.get(event_id))
    return response


@events.route('/<int:id>')
def participate_event(id):
    '''
    Ajax handler for registered user
    '''
    if g.user.is_anonymous():
        abort(403)

    response = {'status': 'ok'}
    event = Event.query.get_or_404(id)

    if g.user in event.participants:
        response = {'status': 'err', 'message': 'You are already registered'}
    else:
        event.participants.add(g.user)

    return jsonify_status_code(response)


@events.route('/<int:id>')
def participate_event_new_user(id):
    '''
    Ajax handler for not registered user
    '''
    event = Event.query.get_or_404(id)
    user = User.create(request.form)

    event.participants.add(user)

    response = {'status': 'ok',
                'message': 'Check your inbox for compleate registration'}

    return jsonify_status_code(response)
