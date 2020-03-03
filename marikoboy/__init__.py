#!/usr/bin/env python3
from flask import Flask
from flask_socketio import SocketIO
import logging


app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True
socketio = SocketIO(app)

from marikoboy import routes