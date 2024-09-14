import requests

from mongodb_api import get_page_token


def send_message_to_fb_messenger(recipient_id: str, message_text: str, page_id: str) -> None:
    try:
        page_token = get_page_token(page_id=page_id)
        url = f"""https://graph.facebook.com/v17.0/me/messages?access_token={page_token["token"]}"""
        data = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("FB MESSENGER MESSAGE SENT SUCCESSFULLY.")
        else:
            print("FB MESSENGER MESSAGE SENT FAILED.")
    except:
        print("FB MESSENGER MESSAGE SENT FAILED.")
