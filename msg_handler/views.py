from flask import request, make_response, url_for, render_template, abort, send_from_directory
from msg_handler import app
import requests
import simplejson
from datetime import datetime, date
from msg_handler import logger


@app.route('/')
def index():
    """

    """
    msg = "Hello world."
    return make_response(msg)


@app.route('/message/')
def message():
    """

    """

    return make_response('Message view.')


@app.route('/event/')
def event():
    """

    """

    return make_response('Event view.')