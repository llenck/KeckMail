import os, json
from urllib.parse import quote, unquote
from datetime import datetime

import config
from mail import Mail

async def save_mail(mail):
    prefix = config.fs_prefix + "/" + quote(mail.data["receiver"], safe="")
    
    time = datetime.utcfromtimestamp(mail.data["received_at"])
    path = prefix + "/" + quote(mail.data["sender"], safe="") + "-" + \
        time.strftime("%Y-%m-%d.%H:%M:%S") + ".json"

    try:
        os.mkdir(prefix)

    except FileExistsError:
        pass

    with open(path, "w") as f:
        f.write(mail.serialize())
