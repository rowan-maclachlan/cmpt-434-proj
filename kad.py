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

log = logging.getLogger('kademlia')
log.setLevel(logging.DEBUG)

loop = asyncio.get_event_loop()
loop.set_debug(True)

# Create Kademlia node
node = Node(my_ip, my_port)

loop.run_until_complete(node.listen())
# Bootstrap node if applicable
if (boot_ip is not None) and (boot_port is not None):
    loop.run_until_complete(node.bootstrap(boot_ip, boot_port))

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

node.stop()
loop.close()
