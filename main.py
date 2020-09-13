import asyncio

import config
from client_loop import client_loop

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.start_server(client_loop, port=config.port,
    host=config.host, reuse_port=True))

try:
    loop.run_forever()
except:
    print("\nBye!")
    pass
