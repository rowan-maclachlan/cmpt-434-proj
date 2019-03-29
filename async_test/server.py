import sys
sys.path.append('/home/silentknight/School/CS434/434proj/cmpt-434-proj')

import asyncio
from rpcudp.protocol import RPCProtocol



class RPCServer(RPCProtocol):
    # Any methods starting with "rpc_" are available to clients.
    def rpc_sayhi(self, sender, name):
        # This could return a Deferred as well. sender is (ip,port)
        return [1,2,3,4,5]

# start a server on UDP port 1234
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCServer, local_addr=('127.0.0.1', 1234))
transport, protocol = loop.run_until_complete(listen)
loop.run_forever()
