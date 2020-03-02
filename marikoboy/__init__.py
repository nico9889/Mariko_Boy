#!/usr/bin/env python3
from flask import Flask
import logging


app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True

from marikoboy import routes