import asyncio
from rpcudp.protocol import RPCProtocol
import sys


@asyncio.coroutine
def sayhi(protocol, address):
    # result will be a tuple - first arg is a boolean indicating whether a
    # response was received, and the second argument is the response if one
    #     was received.
    result = yield from protocol.sayhi(address, "Snake Plissken")
    print(result[1] if result[0] else "No response received.")
    
# Start local UDP server to be able to handle responses
port = 4567 if len(sys.argv) == 2 else input("Which port? ")

loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(\
        RPCProtocol, local_addr=('127.0.0.1', port))
transport, protocol = loop.run_until_complete(listen)

# Call remote UDP server to say hi
func = sayhi(protocol, ('127.0.0.1', 1234))
loop.run_until_complete(func)

print("leaving...")
