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


@app.route('/message/', methods=['GET', 'POST'])
def message():
    """

    """

    logger.debug("MESSAGE endpoint called")
    tmp = request.get_json()
    logger.debug(simplejson.dumps(tmp, indent=4))

    return make_response("OK")


@app.route('/event/', methods=['GET', 'POST'])
def event():
    """

    """

    logger.debug("EVENT endpoint called")
    tmp = request.get_json()
    logger.debug(simplejson.dumps(tmp, indent=4))

    return make_response("OK")