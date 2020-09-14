import json
from datetime import datetime

class Mail:
    def __init__(self, src_json=None):
        if src_json == None:
            self.data = {
                "sender": "",
                "receiver": "",
                "forwarded": False,
                "veryfied": False,
                "received_at": int(datetime.now().timestamp()),
                "content": ""
            }

        else:
            self.data = json.loads(src_json)

    def serialize():
        return json.dumps(json.dumps(self.data))
