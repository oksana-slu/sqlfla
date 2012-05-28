import os
import sys

app_path = os.path.abspath(os.path.dirname(__file__))
app_path in sys.path or sys.path.insert(0, app_path)

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment
from flask.ext.babel import Babel

from .main import bootstrap_js, vendor_js, user_js
import settings


app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)
assets = Environment(app)
babel = Babel(app)

assets.register("bootstrap_js", bootstrap_js)
assets.register("vendor_js", vendor_js)
assets.register("user_js", user_js)

# from core import core
from auth import auth
from events import events


# app.register_blueprint(core, url_prefix="")
app.register_blueprint(auth, url_prefix="")
app.register_blueprint(events, url_prefix="/events")

# print app.url_map
