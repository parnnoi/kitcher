import os
from dotenv import load_dotenv

load_dotenv()

domain = os.getenv('API_DOMAIN')

# host = "sql12.freesqldatabase.com"
# user = "sql12661888"
# password = "qGTLcNPmDQ"
# db = "sql12661888"

# db = os.getenv("kitcher")
# user = "m1jbcw564xabe9b9e1ax"
# host = "aws.connect.psdb.cloud"
# password = "pscale_pw_C6Tn0cZ3SHIQUvvuGEfbNTHvMAiYmscTLDuB8ExGNT3"

db = os.getenv('PLANETSCALE_API_DB')
user = os.getenv('PLANETSCALE_API_USER')
host = os.getenv('PLANETSCALE_API_HOST')
password = os.getenv('PLANETSCALE_API_PASSWORD')