from rpcudp.protocol import RPCProtocol
import logging

log = logging.getLogger(__name__)

class Protocol(RPCProtocol):
    """ 
    class::Protocol
    
    This class defines the callback methods used by rpcudp.  RPCProtocol is a
    small library built on top of asyncio that provides a remote procedure call
    interface over UDP.
    See https://github.com/bmuller/rpcudp for implementation details.
    Callback methods must be preceded by 'rpc_'
    """

    def __init__(self, source, table, data):
        """
        source : Contact
            This Kademlia Node 
        table : RoutingTable 
            This Kademlia Node's buckets 
        data : {}
            A dictionary in which to store key value pairs
        """
        """ Who am I in Kademlia? """
        _this_node = source 
        """ My K Buckets """
        _table = table
        """ Where I store key-value pairs that I'm reponsible for """
        _data = data


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
        log.debug(f"Got request from {senderId} at {sender[0]}:{sender[1]}")
        log.info(f"rpc_ping: from {senderId} at {sender[0]}:{sender[1]}")
        source = Contact(senderId, sender[0], sender[1])
        add_new_node(source)
        return _this_node.getId()
    

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
        response = await self.ping(address, _this_node.getId())
        return self.handle_response(response, contact)

    def rpc_store(self, sender, senderId, key, value):
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
        source = Contact(id, sender[0], sender[1])
        add_new_node(source)
        data[key] = value
        return True


    async def try_store(self, contact, key, value):
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
        response = await self.store(address, _this_node.getId(), key, value)
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
        [Contact] : A list of Contacts 
        """
        log.debug(f"Got request from {senderId} at {sender[0]}:{sender[1]}")
        log.info(f"rpc_find_node: finding closest neighbours of node {targetId}")
        source = Contact(id, sender[0], sender[1])
        add_new_node(source)
        # TODO find K nearest neighbours of targetId
        # TODO How do we format this response?
        nearest_neighbours = self._table.find_nearest_neighbours(targetId)
        return nearest_neighbours


    async def try_find_close_nodes(self, contact, targetContact):
        """
        Try to find the node 'targetContact' by sending an RPC to the node
        'contact'.

        Parameters
        ---------
        contact : Contact
            The contact we would like to send the find node RPC to.
        targetContact : Contact
            The contact we would like to find.

        """
        address = (contact.getIp(), contact.getPort())
        response = await self.find_close_nodes(address, _this_node.getId(),
                targetContact.getId())
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
        TODO how do we format this?
        [Contact] : A list of Contacts 
        """
        log.debug(f"Got request from {senderId} at {sender[0]}:{sender[1]}")
        log.info(f"rpc_find_value: finding value associated with {targetKey}")
        source = Contact(senderId, sender[0], sender[1])
        add_new_node(source)
        value = data[targetKey]
        if value is None:
            # If we do not have the value, return nodes which may have it 
            return self.rpc_find_close_nodes(sender, senderId, targetKey)
        else:
            # If we do have the value, we can return it.
            return value 


    def try_find_value(self, contact, targetKey):
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
        response = await self.find_value(address, _this_node.getId(), targetKey)
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
            log.warning(f"Failed to receive response from node "
                        f"{contact.getId()} at {contact.getIp()}:{contact.getPort(}")
            # TODO remove contact from my routing table 
            return response
        else:
            log.debug(f"Received response from node {contact.getId()} "
                      f"at {contact.getIp()}:{contact.getPort()}")
            # TODO update node in routing table
            return response


    def add_new_node(self, contact):
        """
        Add this contact to our routing table if we do not already know about
        them.  If they are new, pass them all the data we are holding that they
        aught to hold
        
        Parameters
        ----------
        contact : Contact
            The Contact we should attempt to add to our routing table.

        Return : Boolean
            True if they were a new node, and false otherwise
        """
        # TODO implement!
        return False
