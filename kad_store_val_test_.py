import sys
sys.path.append('/home/silentknight/School/CS434/434proj/cmpt-434-proj')

import logging
import asyncio

from kademlia.Node import Node
from kademlia.Contact import Contact

async def put_test():
	thread1 = asyncio.create_task(node1.put('345', data1))
	print(asyncio.get_event_loop())
	await thread1
	print(node2.data)

node1 = Node('127.0.0.1', 3400) 


print("node1 id: ", node1.me.getId())
node1.me._dict['id'] = 123
node1.table.add_contact(Contact(345, '127.0.0.1', 3401))

data1 = "test data"

loop = asyncio.get_event_loop()
loop.set_debug(True)

loop.run_until_complete(node1.listen())
	
asyncio.run(put_test())
