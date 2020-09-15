import pymongo
import config

mongo_client = pymongo.MongoClient(mongodb_domain)
db = myclient["KeckMailDB"]
dbcol_mails = db["mails"]

def save_mail(mail):
    dbcol_mails.insert_one(mail)
