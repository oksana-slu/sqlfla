# -*- encoding: utf-8 -*-
from datetime import datetime
from flask.ext.script import Command, Option, prompt, prompt_pass
from flask.ext.security.exceptions import RoleNotFoundError, UserNotFoundError

from eventor import app, db

from eventor.auth.models import Role

# from core.models import Page
from eventor.events.models import EventStory, Event
from eventor.core.models import Page


class CreateSuperuser(Command):
    """ Create superuser with the given email and password
    """
    option_list = (
       Option('--demo', '-d', dest='demo', action='store_true', default=False,
              help="Create user with the default values"),
    )

    def run(self, demo=False):
        if demo:
            email, password = 'demo@demo.de', 'demo'
            print("Creating user with login {0} and password {1}".format(email, password))
        else:
            email = prompt("Provide email for the superuser")
            password = prompt_pass("Provide user {} with the password".format(email))
            confirm = prompt_pass("Confirm password")

            if password != confirm:
                print("Password doesn't match it's confirmation")
                return

        admin_role = self.get_admin_role()

        try:
            user = app.security.datastore.find_user(email=email)
            print 'user:', user
            print("User with email {0.email} already exists".format(user))
        except UserNotFoundError:
            print("Creating user: {} with password: {}".format(email, password))
            app.security.datastore.create_user(email=email, password=password,
                                               roles=[admin_role],
                                               confirmed_at=datetime.utcnow(),
                                               first_name=u'Демо',
                                               last_name=u'Демович')

    def get_admin_role(self):
        role_name = app.config['ADMIN_ROLE']
        try:
            role = app.security.datastore.find_role(role_name)
        except RoleNotFoundError:
            role = app.security.datastore.create_role(name=role_name)

        return role


class InitDB(Command):
    """ Reinitialize database
    """

    def run(self):
        db.drop_all()
        db.create_all()


superuser = {
    'email': 'demo@demo.de',
    'password': 'demo',
    'first_name': u'Демо',
    'last_name': u'Демович',
    'roles': ['admin'],
    'confirmed_at': datetime.utcnow()
}

pages = [
    {'name': u"Confirmation email sent",
     'content': u"""
        Hey mister! You are in one step from accessing our service. Please
        confirm your email address following the link we've just sent to your
        email box."""},
]

event_lines = [
    {'name': u"KharkivPy",
     'description': u"Харьковское python коммьюнити"}
]

event_data = {
    'name': 'KharkivPy #100',
    'description': u'Сотая встреча Харьковской группы python-разработчиков',
    'starts_at': datetime(2014, 1, 1, 14, 00),
    'ends_at': datetime(2014, 1, 1, 21, 00),
    'reg_starts': datetime(2012, 1, 1, 21, 00),
    'reg_ends': datetime(2013, 12, 31, 00, 00)
}


class Seed(Command):

    def create_superuser(self):
        self.create_roles()
        return app.security.datastore.create_user(**superuser)

    def create_visitors(self):
        user_data = superuser.copy()
        for i in xrange(1, 100):
            user_data.update({
                'roles': ['user'],
                'email': "demo_{}@demo.de".format(i),
                'first_name': u"Демо {}".format(i)
            })
            yield app.security.datastore.create_user(**user_data)

    def create_roles(self):
        for name in app.config['ROLE_SET']:
            Role.get_or_create(name=name)

    def create_event(self, story, author):
        event = Event(**event_data)
        story.events.append(event)
        for user in self.create_visitors():
            event.participants.append(user)
        return event.save()

    def create_story(self, author):
        for event_line in event_lines:
            event_line['author'] = author
            story = EventStory.create(**event_line)
            return story

    def create_pages(self):
        for page_data in pages:
            page = Page.create(**page_data)
            print("created page {0.name}".format(page))

    def run(self):
        db.drop_all()
        db.create_all()
        self.create_pages()

        superuser = self.create_superuser()
        story = self.create_story(superuser)
        event = self.create_event(story, superuser)
        print event
