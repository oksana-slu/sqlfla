from flask.ext.script import Command, Option, prompt, prompt_pass

from eventor import db
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
            print("Created user with login {0} and password {1}".format(email, password))
        else:
            email = prompt("Provide email for the superuser")
            password = prompt_pass("Provide user {} with the password".format(email))
            confirm = prompt_pass("Confirm password")

            if password != confirm:
                print("Password doesn't match it's confirmation")
                return

        User.create(email=email, password=password, is_superuser=True)


class InitDB(Command):
    """ Reinitialize database
    """

    def run(self):
        db.create_all()
