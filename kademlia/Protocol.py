import asyncio
import logging

from rpcudp.protocol import RPCProtocol
from kademlia.Contact import Contact
from kademlia.utils import distance_to

log = logging.getLogger(__name__)

class Protocol(RPCProtocol):
    """ 
    This class defines the callback methods used by rpcudp.  RPCProtocol is a
    small library built on top of asyncio that provides a remote procedure call
    interface over UDP.
    See https://github.com/bmuller/rpcudp for implementation details

    Parameters
    ----------
    source : :class:`Contact`
        This Kademlia Node 
    table : :class:`RoutingTable`
        This Kademlia Node's buckets 
    data : {}
        A dictionary in which to store key value pairs
    """

    def __init__(self, source, table, data, waitTimeout=5):
        """ Who am I in Kademlia? """
        self.this_node = source 
        """ My K Buckets """
        self.table = table
        """ Where I store key-value pairs that I'm reponsible for """
        self.data = data
        self._waitTimeout = waitTimeout
        self._outstanding = {}


    def rpc_ping(self, sender, senderId):
        """
        If we recieve this RPC, try to add the sender to our routing table.
        Repond with our ID so that the requestor can update their table with
        us.

        Parameters
        ----------
        sender : []
            A 2-element list with the network info of the node making the RPC
        senderId : int
            The ID of the node making the RPC

        Response
        --------
        int : The ID of this Kademlia node
        """
        log.info(f"rpc_ping: from {senderId} at {sender[0]}:{sender[1]}")
        source = Contact(senderId, sender[0], sender[1])
        self.handle_node(source)
        return self.this_node.getId()
    

    async def try_ping(self, contact):
        """
        Try to execute the ping remote procedure call on the node
        'contact'.  This is handled by rpc_ping on the remote node.
        Parameters
        ---------
        contact : Contact
            The contact we would like to ping
        """
        address = (contact.getIp(), contact.getPort())
        response = await self.ping(address, self.this_node.getId())
        return self.handle_response(response, contact)


    def rpc_store_value(self, sender, senderId, key, value):
        """
        Store the value 'value' at key 'key'. 
        
        Parameters
        ----------
        sender : []
            A 2-element list with the network info of the node making the RPC
        senderId : int
            The ID of the node making the RPC
        key : int
            A node ID to find
        value : str

        Returns
        -------
        [Contact] : A list of Contacts 
        """
        log.debug(f"Got request from {senderId} at {sender[0]}:{sender[1]}")
        log.info(f"rpc_store: storing the value {value} at key {key}.")
        source = Contact(senderId, sender[0], sender[1])
        self.handle_node(source)
        self.data[key] = value
        return True


    async def try_store_value(self, contact, key, value):
        """ 
        Make an RPC to store the value 'value' at key 'key' to the Kademlia
        node 'contact'.

        Parameters
        ---------
        contact : Contact
            The contact we want to store to.
        key : int
            The key of the value we want to store.
        value : str
            The value associated with our key.

        """
        address = (contact.getIp(), contact.getPort())
        response = await self.store_value(address, self.this_node.getId(), key, value)
        return self.handle_response(response, contact)


    def rpc_find_close_nodes(self, sender, senderId, targetId):
        """
        Find and return a list of k Contacts to the sender.  We can even return
        ourselves, but we should not return the sender in our list.
        
        Parameters
        ----------
        sender : []
            A 2-element list with the network info of the node making the RPC
        senderId : int
            The ID of the node making the RPC
        targetId : int
            A node ID to find

        Returns
        -------
        [Contact] : A list of Contacts of up to size K
        """
        log.debug(f"Got request from {senderId} at {sender[0]}:{sender[1]}")
        log.info(f"rpc_find_node: finding closest neighbours of node {targetId}")
        source = Contact(senderId, sender[0], sender[1])
        self.handle_node(source)
        # TODO Don't return the source itself!
        nearest_neighbours = self.table.find_nearest_neighbours(targetId, exclude=source)
        # Return a list of tuple(Contact) so that pmsgpack can successfully
        # pack our Contact objects.
        return list(map(tuple, nearest_neighbours))


    async def try_find_close_nodes(self, contact, targetId):
        """
        Try to find the node 'targetId' by sending an RPC to the node
        'contact'.

        Parameters
        ---------
        contact : Contact
            The contact we would like to send the find node RPC to.
        targetId : int 
            The ID of the contact we would like to find.

        """
        log.info(f"Looking for {targetId} by asking {contact}")
        address = (contact.getIp(), contact.getPort())
        response = await self.find_close_nodes(address, self.this_node.getId(), targetId)
        return self.handle_response(response, contact)


    def rpc_find_value(self, sender, senderId, targetKey):
        """
        Find the value associated with the given key. If the corresponding
        value is present on the recipient, the associated data is returned.
        Otherwise, the RPC is equivalent to find_close_nodes. 

        According to the implementation specification this is a primitive
        operation, not an iterative one.

        Parameters
        ----------
        sender : []
            A 2-element list with the network info of the node making the RPC
        senderId : int 
            The ID of the node making the RPC
        targetKey : int
            A key to find

        Returns
        -------
        [Contact], str : A list of Contacts of up to size K, 
                         the string being sought
        """
        log.debug(f"Got request from {senderId} at {sender[0]}:{sender[1]}")
        log.info(f"rpc_find_value: finding value associated with {targetKey}")
        source = Contact(senderId, sender[0], sender[1])
        self.handle_node(source)
        if targetKey in self.data:
            return self.data[targetKey]
        else:
            # If we do not have the value, return nodes which may have it 
            return self.rpc_find_close_nodes(sender, senderId, targetKey)


    async def try_find_value(self, contact, targetKey):
        """
        Try to find the value associated with targetKey by sending an RPC to the node
        'contact'.

        Parameters
        ---------
        contact : Contact
            The contact we would like to send the find node RPC to.
        targetKey : int
            The key of the value we would like to find 
        """
        address = (contact.getIp(), contact.getPort())
        response = await self.find_value(address, self.this_node.getId(), targetKey)
        return self.handle_response(response, contact)


    def handle_response(self, response, contact):
        """
        Parameters
        ---------
        response : list
            Result has its first element as a boolean.  If the request did not
            time out and the we received a reponse, the first elemenet will be
            true.  Otherwise it will be false.
        contact : Contact
            The Kademlia node we sent the request to.
        Return
        ------
        list : A list in which the first value is a boolean indicating whether
               the request was successful and the second value is the response.

        """
        if not response[0]:
            log.warning(f"""
                    No response from node {contact.getId()}\
                    at {contact.getIp()}:{contact.getPort()}\
                    """)
            self.table.remove(contact)
            return response
        else:
            log.debug(f"Received response from node {contact.getId()} "
                      f"at {contact.getIp()}:{contact.getPort()}")
            self.handle_node(contact)
            return response


    def handle_node(self, contact):
        """
        Add this contact to our routing table if we do not already know about
        them.  If they are new, pass them all the data we are holding that they
        aught to be holding.
        
        Parameters
        ----------
        contact : Contact
            The Contact we should attempt to add to our routing table.

        Return : Boolean
            True if they were a new node, and false otherwise
        """
        if contact in self.table or self.this_node.getId() == contact.getId():
            log.debug(f"Node {contact.getId()} is already in our routing table.")
            return False
        # See Kademlia paper section 2.5 on how to incorporate new nodes.
        # We may have to store all values we have which are closer to the
        # new node than they are to us.
        log.info(f"Adding node {contact.getId()} to our routing table...")

        for key, value in self.data.items():
            log.debug(f"Consider storing {value}...")
            # find neighbours close to the key value
            nearest_contacts = self.table.find_nearest_neighbours(key)
            # If there are fewer than k neighbours, store the key-value to the
            # new node
            if len(nearest_contacts) < self.table.k:
                log.debug(f"Few contacts, storing data to new contact...")
                # schedule the task in the event loop, continue to next data
                asyncio.create_task(self.try_store_value(contact, key, value))
                continue
            # If there are k neighbours, only store the key-value if the new
            # node is closer to the key the our neighbour furthest from the
            # key, and if we are closer to the new node than any of our
            # neighbours.
            nearest_contact = nearest_contacts[0]
            # are we nearer to this key than nearest_contact is?
            were_nearest = \
                    distance_to(self.this_node.getId(), contact.getId()) < \
                    distance_to(nearest_contact.getId(), contact.getId())
            furthest_contact = nearest_contacts[-1]
            # Is contact closer to the key than the furthest contact?
            close_enough_to_store = \
                    distance_to(contact.getId(), key) < \
                    distance_to(furthest_contact.getId(), key)
            if close_enough_to_store and were_nearest:
                log.debug(f"Storing {data} to new contact...")
                asyncio.create_task(self.try_store_value(contact, key, value))

        self.table.add(contact)

        return True
