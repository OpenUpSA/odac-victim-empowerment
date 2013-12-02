from flask import request, make_response, url_for, render_template, abort, send_from_directory
from msg_handler import app
import requests
import simplejson
from datetime import datetime, date
from msg_handler import logger
import requests

#if __name__ == "__main__":
#    f = open('msg_example.json', 'r')
#    msg_test = simplejson.loads(f.read())


main_menu = {
    1: "Immediately after the incident.",
    2: "Going to the Hospital / Clinic.",
    3: "SAPS",
    4: "Court",
    5: "Welfare / NGO\'s"
}

menu_1 = {
    1: "Reporting",
    2: "Health",
    3: "Evidence",
    4: "Intoxication"
}


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


def serialize_options(options_dict):

    options_str = ""
    for key, val in options_dict.iteritems():
        options_str += "\n" + str(key) + ": " + val
    return options_str


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
            try:
                menu_item = int(content)
                reply(message_id, serialize_options(menu_1))
            except Exception:
                if not content:
                    reply(message_id, serialize_options(main_menu))
                else:
                    reply(message_id, 'You have selected %s.' % (content,), session_event="close")
                pass
        except Exception as e:
            logger.exception(e)
            pass
    return make_response("OK")


@app.route('/event/', methods=['GET', 'POST'])
def event():
    """

    """

    logger.debug("EVENT endpoint called")
    tmp = request.get_json()
    logger.debug(simplejson.dumps(tmp, indent=4))
    return make_response("OK")