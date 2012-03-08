from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

import settings


app = Flask(__name__)
app.config.from_object(settings)
db = SQLAlchemy()
db.init_app(app)

from core import core


app.register_blueprint(core, url_prefix="")

print app.url_map
