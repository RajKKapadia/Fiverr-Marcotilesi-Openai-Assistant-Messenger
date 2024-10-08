import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

ERROR_MESSAGE = 'We are facing an issue at this momemnt, please try after sometime.'

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
DATABASE_NAME = os.getenv("DATABASE_NAME")
