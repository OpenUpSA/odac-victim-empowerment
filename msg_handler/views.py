from flask import request, make_response, url_for, render_template, abort, send_from_directory
from msg_handler import app
import requests
import simplejson
from datetime import datetime, date
from msg_handler import logger
import requests


@app.route('/')
def index():
    """

    """
    msg = "Hello world."
    return make_response(msg)


def reply(message_id, content, session_event="resume"):

    access_token = app.config['ACCESS_TOKEN']
    account_key = app.config['ACCOUNT_KEY']
    conversation_key = app.config['CONVERSATION_KEY']
    message_url = 'http://go.vumi.org/api/v1/go/http_api/%s/messages.json' % (
        conversation_key,)

    payload = {
        "in_reply_to": message_id,
        "content": content,
        "session_event": session_event,
    }
    requests.put(message_url, auth=(account_key, access_token),
        data=simplejson.dumps(payload))
    return


@app.route('/message/', methods=['GET', 'POST'])
def message():
    """

    """

    logger.debug("MESSAGE endpoint called")

    if request.method == 'POST':

        msg = request.get_json()
        logger.debug(simplejson.dumps(msg, indent=4))

        try:
            content = msg['content']
            message_id = msg['message_id']

            if not content:
                reply(message_id, 'Hi, what is your name?')
            else:
                reply(message_id, 'Thanks %s!' % (content,), session_event="close")
        except Exception as e:
            logger.exception(e)
            pass

    return make_response("OK")


#@app.route('/event/', methods=['GET', 'POST'])
#def event():
#    """
#
#    """
#
#    logger.debug("EVENT endpoint called")
#    tmp = request.get_json()
#    logger.debug(simplejson.dumps(tmp, indent=4))
#
#    return make_response("OK")