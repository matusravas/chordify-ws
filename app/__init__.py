from flask import Flask
from dotenv import dotenv_values, load_dotenv

app = Flask(__name__)

config = dotenv_values('configs/.store')
ok = load_dotenv('configs/.env')

BASE_URL_SONGS = config.get('BASE_URL_SONGS', None)
BASE_URL_CHORDS = config.get('BASE_URL_CHORDS', None)
AUTH_TOKEN = config.get('AUTH_TOKEN', None)

if not (BASE_URL_SONGS or BASE_URL_CHORDS):
    raise Exception('No BASE_URL_CHORDS || BASE_URL_SONGS specified in .store!')
if not AUTH_TOKEN:
    raise Exception('Authorization token not specified in .env!')