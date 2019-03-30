import logging
import sys
import asyncio

from kademlia.Node import Node

if len(sys.argv) == 3:
    my_ip = sys.argv[1]
    my_port = sys.argv[2]
    boot_ip = None
    boot_port = None
    print(f"Launching new Kademlia network on {my_ip}:{my_port}")

elif len(sys.argv) == 5:
    my_ip = sys.argv[1]
    my_port = sys.argv[2]
    boot_ip = sys.argv[3]
    boot_port = sys.argv[4]
    print(f"Launching new Kademlia node on {my_ip}:{my_port}"\
          f" with bootstrapping node {boot_ip}:{boot_port}")

else:
    print(f"Usage: python3 {sys.argv[0]} <Node IP> <Node port> "\
          f"[<bootstrap IP>] [<bootstrap port>]")
    exit(1)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.setLevel(logging.DEBUG)
log.addHandler(handler)
logrpc = logging.getLogger('rpcudp')
logrpc.setLevel(logging.DEBUG)
logrpc.addHandler(handler)
logasyncio = logging.getLogger('asyncio')
logasyncio.setLevel(logging.DEBUG)
logasyncio.addHandler(handler)

loop = asyncio.get_event_loop()
loop.set_debug(True)

# Create Kademlia node
node = Node(my_ip, my_port)

loop.run_until_complete(node.listen())
loop.run_forever()
