from flask import Flask, Blueprint
from dotenv import dotenv_values, load_dotenv

app = Flask(__name__)

config = dotenv_values('configs/.store')
ok = load_dotenv('configs/.env')

BASE_URL_TABS = config.get('BASE_URL_TABS', None)
AUTH_TOKEN = config.get('AUTH_TOKEN', None)

if not BASE_URL_TABS:
    raise Exception('No BASE_URL_TABS specified in .env!')
if not AUTH_TOKEN:
    raise Exception('Authorization token not specified in .env!')