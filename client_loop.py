import asyncio
from asyncio.exceptions import *
import traceback

import config
from mail import Mail
from handlers import call_handler
from connection_state import ConnectionState
from exceptions import *
from save_mail import try_save_mail

async def client_loop(r, w):
    print("Client connected")

    state = ConnectionState()

    w.write(bytes("220 %s ESMTP KeckMail\r\n" % config.domain, encoding="utf-8"))
    await w.drain()

    try:
        while True:
            # read a single line from the connection
            buf = await r.readuntil()

            resp = ""

            # if we're building a multi-line command and we're not yet done, don't call
            # any handlers
            if not state.multiline_command == None and not buf == b".\r\n":
                if len(state.multiline_command) + len(buf) > config.max_size:
                    raise QuitException("500 onii-chan, there's no way this will fit")

                state.multiline_command += buf
                continue

            # if we just got the last part of a multi-line command, call a handler
            elif not state.multiline_command == None:
                resp = call_handler(state,
                    state.multiline_command, state.next_multiline_handler)

                state.multiline_command = None
                state.next_multiline_handler = None

            # otherwise just call a handler based on the first word of buf
            else:
                command_name = buf.split(b" ")[0].strip(b"\r\n\t")

                resp = call_handler(state, buf, command_name)

            # immediately push the answer to the client, as it would have to wait
            # for it before sending more commands
            w.write(bytes(resp + "\r\n", encoding="utf-8"))
            await w.drain()

    except QuitException as e:
        w.write(bytes(e.message + "\r\n", encoding="utf-8"))
        await w.drain()

    except IncompleteReadError:
        print("Client disconnected")

    except Exception as e:
        # traceback is dumb and will sometimes cause exceptions
        try:
            print("Disconnected abruptly: %s" % traceback.format_exc(e))
        except Exception:
            print("Disconnected abruptly: %s" % repr(e))
            pass

    w.close()
    await w.wait_closed()

    print("Received an email: %s" % state.mail.serialize())
    try_save_mail(state.mail)
