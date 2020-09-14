class QuitException(Exception):
    def __init__(self, msg=None):
        self.message = msg
