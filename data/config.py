import os
from dotenv import load_dotenv

load_dotenv(override=True)

token = os.getenv('BOT_TOKEN')

admins = [
    433364417,  # @pheezz
    983166886,  # @ixeor

]

db_connection_parameters = {
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_USER_PASSWORD'),
    "host": os.getenv('DB_HOST'),
    "port": os.getenv('DB_PORT'),
    "database": os.getenv('DB_NAME')
}
