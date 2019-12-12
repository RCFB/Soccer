from flask import Flask
from flask_session import Session
import os

app = Flask(__name__)

app.config.update(SECRET_KEY=os.environ.get('FLASK_SECRET_KEY'))

app.config.update(SESSION_TYPE='filesystem')
Session(app)

from . import soccer_controller
from . import auth_controller
from . import command_line_interface

