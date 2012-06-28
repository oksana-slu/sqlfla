# -*- encoding: utf-8 -*-
from flaskext.script import Command

from . import app, db
from auth.models import Role
from core.models import Page


pages = [
    {'name': "Confirmation email sent",
     'content': """
        Hey mister! You are in one step from accessing our service. Please
        confirm your email address following the link we've just sent to your
        email box."""}
]


class Seed(Command):

    def create_roles(self):
        for name in [app.config['USER_ROLE'], app.config['ADMIN_ROLE']]:
            Role.get_or_create(name=name)

    def create_pages(self):
        for page_data in pages:
            page = Page.create(**page_data)
            print("created page {0.name}".format(page))

    def run(self):
        db.drop_all()
        db.create_all()
        self.create_roles()
        self.create_pages()
