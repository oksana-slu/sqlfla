from flask.ext.script import Command, Option, prompt, prompt_pass
from flask.ext.security.exceptions import RoleNotFoundError, UserNotFoundError

from eventor import app, db
from auth.models import User


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
                                               roles=[admin_role])

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
