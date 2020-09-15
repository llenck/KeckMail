import os

port = 2525
host = "0.0.0.0"
domain = "smtp.example.com"
max_size = 65535

db_backend = "save_mail_fs"
fs_prefix = os.path.dirname(os.path.realpath(__file__)) + "/data"

mongodb_domain = "mongodb://localhost:27017/"

# make sure people can run this example config
try:
    os.mkdir(fs_prefix)
except:
    pass
