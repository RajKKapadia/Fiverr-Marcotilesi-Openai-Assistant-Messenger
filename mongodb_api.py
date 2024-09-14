from datetime import datetime

from pymongo import MongoClient

import config

client = MongoClient(config.CONNECTION_STRING)
db = client[config.DATABASE_NAME]
user_collection = db["users"]
thread_collection = db["threads"]


def update_messages(recipient_id: str, query: str, response: str) -> bool:
    '''Update messages for the user and reduce the messages_count by one

    Parameters:
        - recipient_id(str): user telegram id
        - response(str): response of the bot
        - query(str): query of the user

    Returns:
        - bool, 0 for failure and 1 for success
    '''
    message = {
        'query': query,
        'response': response,
        'createdAt': datetime.now().strftime('%d/%m/%Y, %H:%M')
    }
    result = user_collection.find_one_and_update(
        {
            'recipient_id': recipient_id
        },
        {
            '$push': {
                'messages': message
            }
        }
    )
    if not result:
        return False
    else:
        return True


def create_user(user: dict) -> bool:
    '''Process the whole body and update the db

    Parameters:
        - data(dict): the incoming request from Telegram

    Returns:
        - bool, 0 for failure and 1 for success
    '''
    result = user_collection.insert_one(user)
    return result.acknowledged


def get_user(recipient_id: str) -> dict[str, any] | None:
    '''Get user

    Parameters:
        - recipient_id(str): sender id of the user

    Returns:
        - bool, 0 for failure and 1 for success
    '''
    result = user_collection.find_one(
        {
            'recipient_id': recipient_id
        }
    )
    if not result:
        None
    return result


def get_thread(recipient_id: str) -> dict[str, any] | None:
    """
    Get a thread by recipient_id.

    Parameters:
        - thread_collection (Collection): MongoDB collection for threads
        - recipient_id (str): Recipient ID to search for

    Returns:
        - Optional[dict]: Thread document if found, None otherwise
    """
    result = thread_collection.find_one({"recipient_id": recipient_id})
    return result


def create_thread(thread: dict) -> bool:
    """
    Create a new thread for a recipient_id.

    Parameters:
        - thread_collection (Collection): MongoDB collection for threads
        - thread (dict): Thread document to insert

    Returns:
        - bool: True if the insertion was successful, False otherwise
    """
    result = thread_collection.insert_one(thread)
    return result.acknowledged


def update_thread(recipient_id: str, thread_id: str) -> bool:
    """
    Update an existing thread in the collection.

    Parameters:
        - thread_collection (Collection): MongoDB collection for threads
        - recipient_id (str): Recipient ID of the thread to update
        - update_data (dict): Data to update in the thread document

    Returns:
        - bool: True if the update was successful, False otherwise
    """
    result = thread_collection.find_one_and_update(
        {
            "recipient_id": recipient_id
        },
        {
            "$set": {
                "thread_id": thread_id
            }
        }
    )
    if not result:
        return False
    else:
        return True
