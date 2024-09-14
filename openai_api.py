from datetime import datetime

from openai import OpenAI, NotFoundError

import config
from mongodb_api import create_thread, get_thread

client = OpenAI(
    api_key=config.OPENAI_API_KEY
)


def ask_openai_assistant(query: str, recipient_id: str, messages: list[dict[str, str]]) -> str:
    try:
        thread_from_db = get_thread(recipient_id=recipient_id)
        thread = None
        if thread_from_db:
            try:
                thread = client.beta.threads.retrieve(
                    thread_id=thread_from_db["thread_id"]
                )
            except NotFoundError as ne:
                print(ne.message)
                thread = client.beta.threads.create(
                    messages=messages
                )
        else:
            thread = client.beta.threads.create(
                messages=messages
            )
            thread_for_db = {
                'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M'),
                "thread_id": thread.id,
                "recipient_id": recipient_id
            }
            create_thread(thread=thread_for_db)
        print(thread.id)
        _ = client.beta.threads.messages.create(
            thread_id=thread.id,
            content=query,
            role='user'
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=config.ASSISTANT_ID
        )
        print(run.id)
        flag = True
        while flag:
            retrieved_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if retrieved_run.status == 'completed':
                flag = False
        retrieved_messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(retrieved_messages.data[0])
        message_text = retrieved_messages.data[0].content[0].text.value
        return message_text
    except:
        return config.ERROR_MESSAGE
