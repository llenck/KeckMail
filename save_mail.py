import config
from mail import Mail

backend = __import__(config.db_backend)

def try_save_mail(mail):
    if "" in [mail.data["receiver"], mail.data["sender"], mail.data["content"]]:
        print("Discarding mail with missing attributes")
        return

    try:
        print("saving", mail)
        backend.save_mail(mail)

    except Exception as e:
        print("failed to save mail: " + repr(e))
        pass
