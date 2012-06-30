# -*- encoding: utf-8 -*-
from flaskext.script import Command

from . import app, db
from auth.models import Role
from core.models import Page
from events.models import EventLine


pages = [
    {'name': "Confirmation email sent",
     'content': """
        Hey mister! You are in one step from accessing our service. Please
        confirm your email address following the link we've just sent to your
        email box."""},
]

event_lines = [
    {'name': "KharkivPy",
     'description': "Харьковское python коммьюнити"}
]


class Seed(Command):

    def create_roles(self):
        for name in app.config['ROLE_SET']:
            Role.get_or_create(name=name)

    def create_event_line(self):
        for event_line in event_lines:
            EventLine.create(**event_line)

    def create_pages(self):
        for page_data in pages:
            page = Page.create(**page_data)
            print("created page {0.name}".format(page))

    def run(self):
        db.drop_all()
        db.create_all()
        self.create_roles()
        self.create_pages()
        self.create_event_line()
