import logging
import sys
import asyncio

from kademlia.Node import Node

################################################################################

if len(sys.argv) == 5:
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
log.setLevel(logging.INFO)
log.addHandler(handler)
logrpc = logging.getLogger('rpcudp')
logrpc.setLevel(logging.INFO)
logrpc.addHandler(handler)
logasyncio = logging.getLogger('asyncio')
logasyncio.setLevel(logging.INFO)
logasyncio.addHandler(handler)

loop = asyncio.get_event_loop()
loop.set_debug(True)

# Create Kademlia node
node = Node(my_ip, my_port)

print("This process stores and retrieves strings on a"\
      " distributed hash table based off of the Kademlia protocol.")


loop.run_until_complete(node.listen())
if boot_ip is not None and boot_port is not None:
    print("Performing bootstrapping...")
    loop.run_until_complete(node.bootstrap(boot_ip, boot_port))
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("\nQuitting!")
    node.stop()
    loop.stop()
    exit(0)
