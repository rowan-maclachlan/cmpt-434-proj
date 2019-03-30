import logging
import sys
import asyncio

from kademlia.Node import Node


def prompt():
    print("'set <key (str)> <value (str)>' to store data\n"\
          "'get <value (str)>' to retrieve data\n"\
          "'quit' to leave\n")

################################################################################
async def do_get(node, key):
    result = await node.get(key)
    if result is None:
        print("No such key-value exists on the network.")
    else:
        print(result[1] if result[0] else "No response received from peers.")

async def do_set(node, key, value):
    result = await node.put(key, value)
    print(result[1] if result[0] else "No response received.")

async def do_ping(node, ip, port):
    result = await node.ping(ip, int(port))
    print(result[1] if result[0] else "No response received.")

################################################################################
def handle_input(node):
    args = ""
    prompt()
    args = sys.stdin.readline().split(" ")
    
    cmd = args[0].rstrip()
    print(f"Attempting to run {cmd}...")
    if cmd == "get":
        asyncio.create_task(do_get(node, args[1]))
    elif cmd == "set":
        asyncio.create_task(do_set(node, args[1], args[2]))
    elif cmd == "ping":
        asyncio.create_task(do_ping(node, args[1], args[2]))
    elif cmd == "inspect":
        print("Routing table:")
        print(str(node.table))
    elif cmd == "quit":
        # TODO Actually quit lol
        print("Leaving!")
    else:
        print("Invalid command.  Try again.")
################################################################################

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

print("This process stores and retrieves strings on a"\
      " distributed hash table based off of the Kademlia protocol.")


loop.run_until_complete(node.listen())
if boot_ip is not None and boot_port is not None:
    print("Performing bootstrapping...")
    loop.run_until_complete(node.bootstrap(boot_ip, boot_port))
prompt()
loop.add_reader(sys.stdin, handle_input, node)
loop.run_forever()
