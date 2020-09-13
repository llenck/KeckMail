import asyncio
from asyncio.exceptions import *

from mail import Mail

async def client_loop(r, w):
    print("Client connected")
    try:
        while True:
            buf = await r.readuntil()
            w.write(buf)
            await w.drain()

    except IncompleteReadError:
        print("Client disconnected")

    except Exception as e:
        print("Disconnected abruptly: %s" % repr(e))