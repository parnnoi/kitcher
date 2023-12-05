import os
from dotenv import load_dotenv

load_dotenv()

domain = os.getenv('API_DOMAIN')

db = os.getenv('PLANETSCALE_API_DB')
user = os.getenv('PLANETSCALE_API_USER')
host = os.getenv('PLANETSCALE_API_HOST')
password = os.getenv('PLANETSCALE_API_PASSWORD')