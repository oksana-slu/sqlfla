DEBUG = True
SECRET_KEY = "<change me please!>"
CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = "postgres://nimnull@localhost/flaskchemy"
SQLALCHEMY_ECHO = False

ADMIN_ROLE = 'admin'
USER_ROLE = 'user'
MANAGER_ROLE = 'manager'
ROLE_SET = [ADMIN_ROLE, USER_ROLE, MANAGER_ROLE]

SECURITY_CONFIRM_EMAIL = True
SECURITY_PASSWORD_HASH = 'sha256_crypt'
SECURITY_DEFAULT_ROLES = [USER_ROLE]
SECURITY_URL_PREFIX = '/s'
SECURITY_POST_REGISTER_VIEW = '/page/confirmation-email-sent'
SECURITY_POST_LOGIN_VIEW = '/profile/'

ADMINS = ('nimnull@gmail.com',)

from local_settings import *
