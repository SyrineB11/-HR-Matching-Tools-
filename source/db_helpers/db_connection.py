import motor.motor_asyncio
from source.configuration.config import settings
url = "mongodb://"+settings.db_username+':' + \
    settings.db_password+"@"+settings.db_service
client = motor.motor_asyncio.AsyncIOMotorClient(url)

db = client.extaction
