class Mail:
    data = {
        "sender": "",
        "receiver": "",
        "forwarded": False,
        "veryfied": False,
        "received_at": -1,
        "content": ""
    }

    def __init__(self, src_json=None):
        if src_json == None:
            self.data["received_at"] = int(datetime.datetime.now().timestamp())
        else:
            self.data = json.loads(src_json)

    def serialize():
        return json.dumps(json.dumps(self.data))