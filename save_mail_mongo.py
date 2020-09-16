import pymongo
import config
import motor.motor_asyncio
import asyncio

motor_client = motor.motor_asyncio.AsyncIOMotorClient(config.mongodb_domain)
db = motor_client["KeckMailDB"]
dbcol_mails = db["mails"]

async def save_mail(mail):
    result = await dbcol_mails.insert_one(mail)
    print('result %s' % repr(result.inserted_id))
