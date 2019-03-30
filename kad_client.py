import logging
import sys
import asyncio

from kademlia.Node import Node

if len(sys.argv) == 3:
    my_ip = sys.argv[1]
    my_port = sys.argv[2]
    print(f"Connecting to new Kademlia node at {my_ip}:{my_port}")
else:
    print(f"Usage: python3 {sys.argv[0]} <Node IP> <Node port>")
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

print("This process stores and retrieves strings on a"\
      " distributed hash table based off of the Kademlia protocol.")

command = ""
instructions = "'set <key (str)> <value (str)>' to store data\n"\
               "'get <value (str)>' to retrieve data\n"\
               "'quit' to leave\n"

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

while(1):
    try:
        args = input(instructions).split(" ")

        if args[0] == "get":
            print(f"do get {args[1]}...")
            loop.run_until_complete(do_get(node, args[1]))
        elif args[0] == "set":
            print(f"do set {args[1]} {args[2]}...")
            loop.run_until_complete(do_set(node, args[1], args[2]))
        elif args[0] == "ping":
            loop.run_until_complete(do_ping(node, args[1], args[2]))
        elif args[0] == "inspect":
            print(str(node.table))
        elif args[0] == "quit":
            print("Leaving!")
            break
        else:
            print("Invalid command.  Try again.")
    except IndexError:
        print("Invalid command.  Try again.")
    except KeyboardInterrupt:
        print("Leaving!")
        break
