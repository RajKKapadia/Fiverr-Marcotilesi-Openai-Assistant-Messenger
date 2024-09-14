import threading
from datetime import datetime

from flask import Flask, request


from mongodb_api import create_page_token, create_user, get_user, update_messages
from openai_api import ask_openai_assistant
from fb_graph_api import send_message_to_fb_messenger
import config
from utils import format_messages

app = Flask(__name__)


@app.route('/facebook', methods=['GET'])
def facebook_get():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    try:
        if mode == 'subscribe' and token == config.VERIFY_TOKEN:
            print('WEBHOOK_VERIFIED')
            return challenge, 200
        else:
            return "BAD_REQUEST", 403
    except:
        return "BAD_REQUEST", 403


def call_ask_openai_assistant_and_send_message_to_fb_messenger(query: str, recipient_id: str, page_id: str) -> str:
    user = get_user(recipient_id)
    if user:
        formatted_messages = format_messages(messages=user['messages'][-5:])
    else:
        formatted_messages = []
    response = ask_openai_assistant(
        query, recipient_id, formatted_messages)
    send_message_to_fb_messenger(
        recipient_id=recipient_id, message_text=response, page_id=page_id)
    if user:
        update_messages(recipient_id=recipient_id,
                        query=query, response=response)
    else:
        message = {
            'query': query,
            'response': response,
            'createdAt': datetime.now().strftime('%d/%m/%Y, %H:%M')
        }
        user = {
            'recipient_id': recipient_id,
            'messages': [message],
            'channel': 'Facebook Messenger',
            'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
        }
        create_user(user)


@app.route('/facebook', methods=['POST'])
def facebook_post():
    try:
        print('A new Facebook Messenger request...')
        body = request.get_json()
        page_id = body["entry"][0]["id"]
        recipient_id = body['entry'][0]['messaging'][0]['sender']['id']
        query = body['entry'][0]['messaging'][0]['message']['text']
        print(query)
        print(recipient_id)
        print(page_id)
        threading.Thread(target=call_ask_openai_assistant_and_send_message_to_fb_messenger,
                         args=(query, recipient_id, page_id)).start()
        print('Request success.')
    except:
        print('Request failed.')
        pass
    return 'OK', 200


@app.route('/add/page-token', methods=['POST'])
def handle_add_page_token():
    try:
        print('Adding new page token.')
        body = request.get_json()
        page_id = body["page_id"]
        token = body["token"]
        page_token = {
            "page_id": page_id,
            "token": token,
            "createdAt": datetime.now().strftime("%d/%m/%Y, %H:%M")
        }
        flag = create_page_token(page_token=page_token)
        if flag:
            return "OK", 201
        else:
            return "BAD_REQUEST", 403
    except:
        return "BAD_REQUEST", 403
