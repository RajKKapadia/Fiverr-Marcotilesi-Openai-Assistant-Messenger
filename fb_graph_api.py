import requests

import config


def send_message_to_fb_messenger(recipient_id: str, message_text: str) -> None:
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={config.FB_PAGE_ACCESS_TOKEN}"
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("FB MESSENGER MESSAGE SENT SUCCESSFULLY.")
    else:
        print("FB MESSENGER MESSAGE SENT FAILED.")
