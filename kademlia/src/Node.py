import params as p
import hashing as hashing
import asyncio
import RoutingTable 
import logging
import Contact
import Protocol

class Node(object):
    """ 
    class::Node
    """

    def __init__(self, host, port):
        """
        host : str
            The hostname this node resides on
        port : str
            The port this node will listen for connections on
        """
        """ Who am I in Kademlia? """
        _me = Contact(hashing.new_id(), host, port)
        logging.info(f"Created a new node at {host}:{port} with ID {_me.getId()}")
        """ My K Buckets routing table """
        _buckets = RoutingTable(p.params[B], p.params[K])
        """ Where I store key-value pairs that I'm reponsible for """
        _data = {}
        _transport = None
        _protocol = None

    def _getHost(self):
        return self._me.getHost()

    def _getPort(self):
        return self._me.getPort()

    def _create_protocol(self):
        return Protocol(_me, _buckets, _data)

    async def listen(self):
        """
        Listen for requests from other nodes
        """
        asyncio.get_event_loop()
        listen = loop.create_datagram_endpoint(
                self._create_protocol,
                local_addr=(_getHost(), _getPort()))

        logging.info("Listening on {}:{}".format(_getHost(), _getPort()))

        self._transport, self._protocol = await listen
        
        
    async def ping(self, ip, port):
        logging.debug(f"Attempting to ping {ip}:{port}")
        return await self._protocol.try_ping(Contact(None, ip, port))

