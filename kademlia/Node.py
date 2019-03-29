import sys
sys.path.append('/home/silentknight/School/CS434/434proj/cmpt-434-proj')  

import asyncio
import logging
import os

from kademlia.Protocol import Protocol
from kademlia.RoutingTable import RoutingTable 
from kademlia.Contact import Contact
import kademlia.params as p
import kademlia.hashing as h

log = logging.getLogger(__name__)

class Node():
    """
    The Node object provide the top level interfaces to the Kademlia DHT that
    an application programmer would use.  After :func:`bootstrapping
    <bootstrap>` a node, the program can use :func:`get` and :func:`put`
    commands to interact with the DHT.

    ip : str
        The IP address this node listens to connections on.
    port : str
        The port this node will listen for connections on.
    """

    def __init__(self, ip, port):
        self.me = Contact(h.new_id(), ip, port)
        """ :class:`Contact` : Who am I in Kademlia? """
        self.table = RoutingTable(p.params[p.B], p.params[p.K], self.me.getId())
        """ :class:`RoutingTable` : My K Buckets routing table """ 
        self.data = {}
        """ dict{} : Where I store key-value pairs that I'm responsible for """
        self._transport = None
        self.protocol = None


    def _getHost(self):
        return self.me.getIp()


    def _getPort(self):
        return self.me.getPort()


    def _createprotocol(self):
        return Protocol(self.me, self.table, self.data)


    def stop(self):
        """
        Close network connections and terminate asyncio loops.
        """
        if self._transport is not None:
            self._transport.close()


    async def listen(self):
        """
        Listen for requests from other nodes.
        """
        loop = asyncio.get_event_loop()
        
        # Create endpoint with our Protocol, RPCProtocol and asyncio subclass
        listen = loop.create_datagram_endpoint(
                self._createprotocol, (self._getHost(), self._getPort()))

        log.info("Listening on {_getHost()}:{_getPort()}")

        self._transport, self.protocol = await listen
        # TODO schedule table refreshing (low priority)
        
    
    async def put(self, key, value):
        """
        Attempt to store the key:value pair provided onto the DHT.

        Parameters
        ----------
        key : str
            The key you wish to you use store the value at.
        value : str
            The value stored on the key.
    
        Return
        ------
        TODO What do we return here?
        """
        log.info(f"Attempting to store {value} on the Kademlia network...")
        if type(value) is not str:
            raise TypeError("The value you attempt to store MUST be a string!")
        #if type(key) is not str:
        #    raise TypeError("The key we use MUST be a string!")

        #hashkey = h.hash_function(key) 

        neighbours = self.protocol.table.find_nearest_neighbours(key)
        if len(neighbours) == 0:
            # TODO If we have no other nodes on which to store it... shouldn't
            # we store it locally?
            log.error("This node has no record of any other nodes!")
            log.info("Stored {value} at {self.me.getId()}")
            return None

        # TODO get a list of the nodes we should store this value on.
        # TODO this should not be only our known neighbours - we should query
        # them for closer contacts.
        return await self.protocol.try_store_value(neighbours[0], key, value)


    async def get(self, key):
        """
        Try to retrieve the value keyed on the key from the Kademlia network.
        If the value can't be retreived or if it doesn't exist on the network,
        return None.
        
        Parameters
        ----------
        key : str
            The key we want to find on the network.
        
        Return
        ------
        str : The value the key maps to, or None if it is not found.
        """
        log.info(f"Attempting to retrieve the value of {key} from the Kademlia network.")

        hashkey = h.hash_function(key)

        if data[hashkey] is not None:
            return data[hashkey]
        
        # Get a list of close nodes in our routing table
        neighbours = self.protocol.table.find_nearest_neighbours(hashkey)
        if len(neighbours) == 0:
            log.error("This node has no record of any other nodes!")
            return None

        # TODO we need to successively query nodes we find closer and closer to
        # our key.
            

    async def bootstrap(self, ip, port):
        """
        Bootstrap this node into the Kademlia network of the node at the IP and
        port provided.

        Parameters
        ----------
        ip : str
            The IP of the bootstrap node on the Kademlia network
        port : str
            The port the the bootstrapping node is listening on.

        Return
        ------
        None
        """
        address = (ip, port)
        response = await self.protocol.ping(address, self.me.getId())
        if response[0]:
            log.info(f"Bootstrapping off of {ip}:{port}")
            new_contact = Contact(response[1], ip, port)
        else:
            log.error(f"Failed to bootstrap off of {ip}:{port}")
            return
        # TODO perform a search for myself... Do a node find on self.me.getId()
        return await self.protocol.try_find_close_nodes(new_contact, self.me)

