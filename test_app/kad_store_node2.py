import sys
sys.path.append('/home/silentknight/School/CS434/434proj/cmpt-434-proj')

import logging
import asyncio

from kademlia.Node import Node
from kademlia.Contact import Contact


node2 = Node('127.0.0.1', 3401)
node2.me._dict['id'] = 345
node2.table.add_contact(Contact(123, '127.0.0.1', 3400))

loop = asyncio.get_event_loop()

node2.protocol = node2._createprotocol()

transport, porotocol = loop.run_until_complete(node2.listen())
loop.run_forever()