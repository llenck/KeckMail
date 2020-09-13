import config

def helo_handler(mail, command):
    return "250 %s, at your service uwu" % config.domain

def ehlo_handler(mail, command):
    return "250-%s, at your service uwu\r\n" % config.domain + \
           "250 SIZE %d" % config.max_size

handlers = {
    b"HELO": helo_handler,
    b"EHLO": ehlo_handler,
}