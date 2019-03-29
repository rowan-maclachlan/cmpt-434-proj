import sys
sys.path.append('/home/silentknight/School/CS434/434proj/cmpt-434-proj')

import logging
import asyncio

from kademlia.Node import Node

async def put_test():
	thread1 = asyncio.create_task(node1.put(node2.me.getId(), data1))
	print(asyncio.get_event_loop())
	await thread1
	print(node2.data)

node1 = Node('127.0.0.1', 3400) 
node2 = Node('127.0.0.1', 3401)

print("node1 id: ", node1.me.getId())
print("node2 id: ", node2.me.getId())

node1.table.add_contact(node2.me)
node2.table.add_contact(node1.me)

data1 = "test data"

loop = asyncio.get_event_loop()
loop.set_debug(True)

node1.protocol = node1._createprotocol()
node2.protocol = node2._createprotocol()

loop.run_until_complete(node1.listen())
loop.run_until_complete(node2.listen())
	
asyncio.run(put_test())
