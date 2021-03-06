import asyncio
import logging

from kademlia.Protocol import Protocol
from kademlia.RoutingTable import RoutingTable 
from kademlia.Contact import Contact
from kademlia.KademliaSearch import KademliaSearch
from kademlia.KademliaSearch import KademliaStoreSearch
from kademlia.KademliaSearch import KademliaValueSearch
from kademlia.KademliaSearch import KademliaNodeSearch
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
    
    protocol_class = Protocol 

    def __init__(self, ip, port):
        self.me = Contact(h.new_id(), ip, int(port))
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


    def _create_protocol(self):
        """
        Most of connection oriented event loop methods (such as
        loop.create_connection()) usually accept a protocol_factory argument
        used to create a Protocol object for an accepted connection,
        represented by a Transport object. Such methods usually return a tuple
        of (transport, protocol). (asyncio protocol python docs)
        """
        return self.protocol_class(self.me, self.table, self.data)


    def stop(self):
        """
        Close network connections and terminate asyncio loops.
        """
        # TODO close refresh loops here when applicable
        # TODO but is this really necessary?
        if self._transport is not None:
            self._transport.close()


    async def listen(self):
        """
        Listen for requests from other nodes.

        Transports and Protocols are used by the low-level event loop APIs such
        as loop.create_connection(). They use callback-based programming style
        and enable high-performance implementations of network or IPC protocols
        (e.g. HTTP).
        """
        loop = asyncio.get_event_loop()
        
        # Create endpoint with our Protocol, RPCProtocol and asyncio subclass
        # See self._create_protocol.  Set optional argument local_addr.
        # self._create_protocol must be a callable returning a protocol
        # implementation.
        # local_addr is used to bind the socket to locally. The local_host and
        # local_port are looked up using getaddrinfo().
        listen = loop.create_datagram_endpoint(
                self._create_protocol, 
                local_addr=(self._getHost(), self._getPort()))

        log.info(f"Listening on {self._getHost()}:{self._getPort()}")

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
        if type(key) is not str:
            raise TypeError("The key we use MUST be a string!")

        hashkey = h.hash_function(key) 

        # Kademlia spec suggests that we should make calls to 'alpha' node per
        # iteration.  TODO take params out of class and inject them all
        # instead?
        neighbours = self.table.find_nearest_neighbours(hashkey, how_many=p.params[p.ALPHA])
        if len(neighbours) == 0:
            # TODO If we have no other nodes on which to store it... shouldn't
            # we store it locally?
            log.error("This node has no record of any other nodes!")
            log.info("Stored {value} at node {self.me}")
            self.data[hashkey] = value
            # TODO these reponses need to be unified and formatted the same
            return [ True, { hashkey : value } ]
        log.debug(f"seeding with {neighbours}")
        store_search = KademliaStoreSearch(self.me, self.protocol, hashkey, value, neighbours)

        responses = await store_search.search(self.protocol.try_find_close_nodes)
        return responses[0]


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
        # TODO HIGH PRIORITY
        log.info(f"Attempting to retrieve the value of {key} from the Kademlia network.")
        if type(key) is not str:
            raise TypeError("The key we use MUST be a string!")

        hashkey = h.hash_function(key)

        if hashkey in self.data:
            return [ True, self.data[hashkey] ]
        
        # Get a list of close nodes in our routing table
        neighbours = self.table.find_nearest_neighbours(hashkey)
        if len(neighbours) == 0:
            log.error("This node has no record of any other nodes!")
            return [ False, None ]

        value_search = KademliaValueSearch(self.me, self.protocol, hashkey, neighbours)
        responses = await value_search.search(self.protocol.try_find_value)
        return responses
            

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
        address = (ip, int(port))
        response = await self.protocol.ping(address, self.me.getId())
        if response[0]:
            log.info(f"Bootstrapping off of {ip}:{port}")
            new_contact = Contact(int(response[1]), ip, int(port))
        else:
            log.error(f"Failed to bootstrap off of {ip}:{port}")
            return
        node_search = KademliaNodeSearch(self.me, self.protocol, self.me.getId(), [ new_contact ] )
        responses = await node_search.search(self.protocol.try_find_close_nodes)
        return responses[0]

    async def ping(self, ip, port):
        address = (ip, int(port))
        response = await self.protocol.ping(address, self.me.getId())
        if response[0]:
            # They answered us with their ID...
            new_contact = Contact(response[1], ip, int(port))
            # So add they to our table!
            self.table.add(new_contact)

        return response # response is a (true/false, ID/None) tuple
