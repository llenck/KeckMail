import config
from exceptions import QuitException
from connection_state import ConnectionState
from mail import Mail


def helo_handler(state, command):
    return "250 %s, at your service uwu" % config.domain

def ehlo_handler(state, command):
    return "250-%s, at your service uwu\r\n" % config.domain + \
           "250-SIZE %d" % config.max_size + \
           "250 SMTPUTF8"

def mail_handler(state, command):
    try:
        sender = command.split(b"<")[1].split(b">")[0]
        state.mail.data["sender"] = sender
        return "250 OK BOOMER"

    except IndexError:
        raise QuitException("500 Verpiss dich KEK")

def data_handler(state, command):
    state.multiline_command = b""
    state.next_multiline_handler = b"data_finish"
    print("set m_command to b\"\" and next_m_handler to %s" %
          state.next_multiline_handler)

    return "354 Gib Daten"

def data_finish_handler(state, line):
    state.mail.data["content"] = line
    return "250 ok boomer"

def rctp_handler(state, line):
    try:
        receiver = line.split(b"<")[1].split(b">")[0]

        if state.mail.data["receiver"] != "":
            print("Warning: client send multiple recipients, discarding" +
                  "the old one (%s)" % state.mail.data["receiver"])

        state.mail.data["receiver"] = str(receiver, encoding="utf-8")
        return "250 OK BOOMER"

    except IndexError:
        raise QuitException("500 Willst du nen Kek in deinen Arsch?")

def quit_handler(state, line):
    raise QuitException("221 go fuckyourself")

def noop_handler(state, line):
    return "250 ok boomer"

def rset_handler(state, line):
    state.mail = Mail()
    return "250 y tho"

def help_handler(state, line):
    return "250 Du nix kriegen Hilfe"

handlers = {
    b"HELO": helo_handler,
    b"EHLO": ehlo_handler,
    b"MAIL": mail_handler,
    b"DATA": data_handler,
    b"data_finish": data_finish_handler,
    b"RCPT": rctp_handler,
    b"QUIT": quit_handler,
    b"RSET": rset_handler,
    b"HELP": help_handler,
}

def call_handler(state, line, cmd):
    try:
        return handlers[cmd](state, line)

    except KeyError:
        return "502 idk bout %s, is it something edible?" % str(cmd, encoding="utf-8")
