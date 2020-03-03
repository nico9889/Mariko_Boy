#!/usr/bin/env python3
from flask import Flask
from flask_socketio import SocketIO
from engineio.payload import Payload
import logging

# Extending this just to avoid errors
Payload.max_decode_packets = 100

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
socketio = SocketIO(app)

from marikoboy import routes