from mail import Mail

class ConnectionState:
    # set to a string that is appended to if receiving a multi line command / data
    multiline_command = None

    # set to a string identifying the handler to be called after the next multi line
    # command / data has been received, as the command may not be part of the data
    next_multiline_handler = None

    mail = Mail()