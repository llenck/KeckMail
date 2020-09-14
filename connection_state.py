from mail import Mail

class ConnectionState:
    def __init__(self):
        # set to a string that is appended to if receiving a multi line command / data
        self.multiline_command = None

        # set to a string identifying the handler to be called after the next multi line
        # command / data has been received, as the command may not be part of the data
        self.next_multiline_handler = None
        
        self.mail = Mail()
