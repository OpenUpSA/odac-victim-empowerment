from flask import request, make_response, url_for, render_template, abort, send_from_directory
from msg_handler import app
from msg_handler.menu import menu
import requests
import simplejson
import time
from datetime import datetime, date
from msg_handler import logger
import requests
from redis import Redis
redis = Redis()

#if __name__ == "__main__":
#    f = open('msg_example.json', 'r')
#    msg_test = simplejson.loads(f.read())


def mark_online(user_id):
    now = int(time.time())
    expires = now + (app.config['ONLINE_LAST_MINUTES'] * 60) + 10
    all_users_key = 'online-users/%d' % (now // 60)
    user_key = 'user-activity/%s' % user_id
    p = redis.pipeline()
    p.sadd(all_users_key, user_id)
    p.set(user_key, now)
    p.expireat(all_users_key, expires)
    p.expireat(user_key, expires)
    p.execute()


def mark_menu(user_id, menu_id):
    now = int(time.time())
    expires = now + (app.config['ONLINE_LAST_MINUTES'] * 60) + 10
    user_key = 'user-menu/%s' % user_id
    p = redis.pipeline()
    p.set(user_key, menu_id)
    p.expireat(user_key, expires)
    p.execute()


def get_current_menu(user_id):
    last_menu = redis.get('user-menu/%s' % user_id)
    if last_menu in [None, "None"]:
        return ""
    return last_menu


def get_online_users():
    current = int(time.time()) // 60
    minutes = xrange(app.config['ONLINE_LAST_MINUTES'])
    return redis.sunion(['online-users/%d' % (current - x)
                         for x in minutes])


@app.route('/')
def index():
    """

    """

    msg = 'Online: %s' % ', '.join(get_online_users())
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


def serialize_options(submenu):

    title = submenu[0]
    items = submenu[1]

    options_str = title

    if not title == "Main menu":
        options_str += "\n0: back"
    for i in range(len(items)):
        item = items[i]
        if len(item) > 1:
            options_str += "\n" + str(i+1) + ": " + item[0]
        else:
            options_str += "\n" + item[0]
    return options_str


def generate_output(user_id, selected_item=None):

    current_menu = get_current_menu(user_id)
    logger.debug("CURRENT MENU: " + str(current_menu))

    if current_menu and selected_item == 0:
        current_menu = current_menu[0:-1]
        selected_item = None

    submenu = menu
    if current_menu and len(current_menu) > 0:
        for i in current_menu:
            submenu = submenu[1][int(i)]

    if current_menu is None:
        current_menu = ""

    if selected_item:
        submenu = submenu[1][selected_item-1]
        current_menu += str(selected_item-1)

    mark_menu(user_id, current_menu)

    str_out = serialize_options(submenu)
    return str_out


@app.route('/message/', methods=['GET', 'POST'])
def message():
    """

    """

    logger.debug("MESSAGE endpoint called")

    if request.method == 'POST':

        msg = request.get_json()
        logger.debug(simplejson.dumps(msg, indent=4))

        try:
            user_id = msg['from_addr']
            content = msg['content']
            message_id = msg['message_id']
            mark_online(user_id)
            selected_item = None
            try:
                selected_item = int(content)
            except (ValueError, TypeError):
                pass
            reply(message_id, generate_output(user_id, selected_item))
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