import asyncio
from asyncio.exceptions import *
import traceback

import config
from mail import Mail
from handlers import handlers
from connection_state import ConnectionState

async def client_loop(r, w):
    print("Client connected")

    state = ConnectionState()

    w.write(bytes("220 %s ESMTP KeckMail\r\n" % config.domain, encoding="ascii"))
    await w.drain()

    try:
        while True:
            # read a single line from the connection
            buf = await r.readuntil()

            resp = ""

            # if we're building a multi-line command and we're not yet done, don't call
            # any handlers
            if not state.multiline_command == None and not buf == ".":
                state.multiline_command += buf
                continue

            # if we just got the last part of a multi-line command, call a handler
            elif not state.multiline_command == None:
                resp = handlers[state.next_multiline_handler](state,
                    state.multiline_command)

                state.multiline_command = None
                state.next_multiline_handler = None

            # otherwise just call a handler based on the first word of buf
            else:
                command_name = buf.split(b" ")[0]

                resp = handlers[command_name](state, buf)

            # immediately push the answer to the client, as it would have to wait
            # for it before sending more commands
            w.write(bytes(resp + "\r\n", encoding="ascii"))
            await w.drain()

            multiline_command = None # clear the current multiline command, if any

    except IncompleteReadError:
        print("Client disconnected")

    except Exception as e:
        print("Disconnected abruptly: %s" % traceback.format_exc(e))