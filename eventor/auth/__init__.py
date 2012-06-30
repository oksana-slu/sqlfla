# -*- encoding: utf-8 -*-
from flask import Blueprint


auth = Blueprint('auth', __name__, template_folder='templates')

import models
import views
import api
