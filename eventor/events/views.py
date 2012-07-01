# -*- encoding: utf-8 -*-
import re
import trafaret as t
from flask import abort, g, render_template, request, redirect, Response, url_for
from flask.ext.security import login_required

from eventor import db
from eventor.auth.models import User
from eventor.core.utils import jsonify_status_code, json_dumps

from . import events
from eventor.events.forms import EventForm, EventStoryForm
from eventor.events.models import Event, EventStory
from eventor.core.utils import jsonify_status_code
from eventor import app

re_container = re.compile('event(?P<id>\d+)Container')

participant = t.Dict({'email': t.Email, 'first_name': t.String, 'last_name': t.String}).ignore_extra('*')


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
    response.data = render_template('events/widget.js', container=c,
                                    event=Event.get(event_id))
    return response


@events.route('/check_participation/<int:id>')
def check_participation(id):
    """ Ajax handler for registered user
    """
    # g.user.is_anonymous()
    callback = request.args.get('callback', 'callback')
    response = {'response': 'ok', 'msg': 'registered'}

    event = Event.query.get_or_404(id)

    if g.user.is_anonymous():
        response = {'response': 'err', 'txt': 'not_registered'}
    elif g.user in event.participants:
        response = {'response': 'err', 'txt': 'already_registered'}
    else:
        response = {'response': 'ok',
                    'txt': {'first': g.user.first_name,
                            'last': g.user.last_name}}
    http_response = Response(content_type='text/javascript')
    http_response.data = "{}({})".format(callback, json_dumps(response))
    return http_response


@events.route('/attend/<int:id>', methods=['GET'])
def attend(id):
    callback = request.args.get('callback', 'callback')
    http_response = Response(content_type='text/javascript')
    response = {'response': 'ok', 'txt': 'You were saved as an event attendee'}
    event = Event.get(id)
    if g.user.is_anonymous():
        print dir(request.form)
        try:
            data = participant.check(request.form.to_dict())
            u = User.create(**data)
            event.participants.append(u)
        except t.DataError as e:
            response = {'response': 'err', 'txt': e.as_dict()}
    else:
        event.participants.append(g.user)
        db.session.commit()

    http_response.data = "{}({})".format(callback, json_dumps(response))
    return http_response
