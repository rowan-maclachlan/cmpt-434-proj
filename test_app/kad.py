import logging
import sys
import asyncio

from kademlia.Node import Node

if len(sys.argv) != 5:
    print(f"Usage: python3 {sys.argv[0]} <Node IP> <Node port> <bootstrap IP> <bootstrap port>")


my_ip = sys.argv[1]
my_port = sys.argv[2]
boot_ip = sys.argv[3]
boot_port = sys.argv[4]

print(f"Launching new Kademlia node on {my_ip}:{my_port}"\
      f" with bootstrapping node {boot_ip}:{boot_port}")

log = logging.getLogger('kademlia')
log.setLevel(logging.DEBUG)

loop = asyncio.get_event_loop()
loop.set_debug(True)

node = Node(my_ip, port)
loop.run_until_complete(node.listen(my_port))
loop.run_until_complete(node.bootstrap(node_ip, node_port))

print("This process stores and retrieves strings on a"\
      " distributed hash table based off of the Kademlia protocol.")

command = ""
instructions = "put <key (str)> <value (str)>\n"\
               "get <value (str)>\n"\
               "quit\n"

while(1):
    args = input(instructions).split(" ")

    try:
        if args[0] == "get":
            print(f"do get {args[1]}")
            print(node.get(args[1]))
        elif args[0] == "set":
            print(f"do set {args[1]} {args[2]}")
            print(node.set(args[1], args[2]))
        elif args[0] == "inspect":
            print(node.get_routing_table())
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
    except Error:
        print("Unknown error.  Kademlia failed.")

server.stop()
loop.close()
