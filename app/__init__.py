from flask import Flask, Blueprint
from dotenv import load_dotenv
import os

app = Flask(__name__)

ok = load_dotenv('configs/.env')
BASE_URL_TABS = os.getenv('BASE_URL_TABS', 'https://www.ultimate-guitar.com')
if not BASE_URL_TABS:
    raise Exception('No BASE_URL_TABS specified in .env!')


router = Blueprint('api', __name__, url_prefix='api')