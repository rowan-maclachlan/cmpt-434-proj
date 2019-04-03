import sys
import logging
import asyncio

from kademlia.Contact import Contact
from kademlia.Contact import ContactHeap
from kademlia.utils import gather_responses
from kademlia.utils import distance_to
from kademlia.utils import merge_heaps
import kademlia.params as p

log = logging.getLogger(__name__)

"""
    TODOs
"""
#TODO: make sure nodes are active before returning them
#TODO: handle iterative store failures and StoreSearch failures


class KademliaSearch():
    """
    The search function used by Kademlia to find nodes in a Kademlia network.
    Asks the alpha closest nodes for the k closest nodes for their k closests nodes.
    Adds the nodes returned to the list of closest nodes and repeats the process
    until either k nodes have been asked, no closer nodes than the previous closest
    was returned, or if the node/value was found. 

    Parameters
    ----------
    initiator : :class:  `Node`
        The node that initaited the search.
    protocol : :class: `Protocol`
        The protocol used for finding nodes. 
    target_id : intorsomething
        The id of the node being searched for.
    contacts : [Contact]
        A list of :class: `Contact`
    k : int
        The maximum number of nodes queried or returned from a query.
    alpha : int
        The number of parrallel queries executed

    Attributes
    ----------
    _initiator : :class:  `Node`
        The node that initaited the search.
    _protocol : :class: `Protocol`
        The protocl used for finding nodes.
    _target_id : intorsomething
        The id of the node being searched for.
    _shortlist : list
        The list of nodes to be queried for their closest neighbours.
    _alpha : int
        The concurrency parameters for kademlia search
    _k_val : int
        The maximum number of queries
    _closest_node : :class: `Node`
        The closest node found so far in this search.
    _response_dict : dict
        a dictionary of responses with keys of the sender's ID who gave the response and values as 
        the response
    """ 


    def __init__(self, initiator, protocol, target_id, contacts, k=p.params['k'], alpha=p.params['alpha']):
        self._initiator = initiator
        """ 
        """
        self._protocol = protocol
        """
        """
        self._target_id = target_id
        """
        """
        self._shortlist = ContactHeap(target_id, k)
        self._shortlist.push_all(contacts)
        log.debug(f"Creating search with peers: {contacts}")
        """
        """
        self._k_val = k
        """
        """
        self._alpha = alpha
        """
        """
        self._closest_node = self._shortlist.peek_first()[1]
        """
        """
        self._contacted = ContactHeap(target_id, k)
        """
        """
        self._active_queries = {}
        """
        """
        self._finished = False
        """
        """


    async def _search(self, rpc_method):
        """
        The base level search that takes place in any of the possible searches in a 
        Kademlia network. This retrives the k closest nodes from the alpha closest neighbours.

        Parameters
        ----------
        rpc_method : :class: `rpc_protocol_method`
            The method used to find nodes.
        """ 
        prev_closest_node = None

        # loop until we have found the node, we have queried k nodes or all
        # responses returned were not closer then our closest yet
        while not self._finished and self._contacted.size() <= self._k_val and self._shortlist.size() > 0:
            peers_to_contact = []
            if (distance_to(self._target_id, self._closest_node.getId())\
                    >= distance_to(self._target_id, self._shortlist.peek_first()[1].getId())):
                self._closest_node = self._shortlist.peek_first()[1]

                for i in range(self._alpha):
                    peers_to_contact.append(self._shortlist.pop())
            else:
                # if there are no closer nodes we search the nearest k nodes instead of a
                # the nearest alpha 
                for i in range(self._k_val):
                    peers_to_contact.append(self._shortlist.pop())
            log.info(f"{self._initiator} preparing to contact: {peers_to_contact}")
            for peer in peers_to_contact:
                self._active_queries[peer] = rpc_method(self._initiator, peer.getId()) 
            responses = await gather_responses(self._active_queries)
            # handles the responses. May terminate the search by setting finished to true,
            # expanding contacted to be greater than k, or determining no nodes found are
            # closer than the closest we have found so far
            result = await self._handle_responses(responses)
            prev_closest_node = self._closest_node

        if not result:
            log.error("ERROR in KademliaSearch: returned None but the search finished")
        return result



class KademliaNodeSearch(KademliaSearch):
    """
    Does a node search, returning a tuple of the success of the search
    and the k closest nodes of the closest node to the target_key. This may be the
    node with the target_key if found or simply some close node. May return 
    fewer than k nodes if there are fewer than k nodes in the closest node's
    bucket.
    """


    def __init__(self, initiator, protocol, target_id, contacts, k=p.params['k'], alpha=p.params['alpha']):
        KademliaSearch.__init__(self, initiator, protocol, target_id, contacts, k, alpha)
        """
        """


    async def search(self, rpc_method):
        """
        The public method for calling the underlying kademlia search.
        """
        return await self._search(rpc_method)


    async def _handle_responses(self, responses_to_handle):
        """
        Handles a dictionary of responses. On completion returns a tuple of the success
        of the search and the k closest nodes that it has found to the target node.

        Parameters
        ----------
        responses : :class: `RPCResponse`


        Returns
        ------
        (successful, k_closest) : tuple
        search_in_progress : boolean
        """ 
        for sender_info, response in responses_to_handle:
            log.info(f"processing {sender_info.getId()}'s data in {self._initiator.getId()}'s search")
            response = RPCResponse(response)
            del(self._active_queries[sender_info.getId()])

            if response.has_happened():
                self._contacted.push(sender_info)
                self._shortlist.push_all(response.get_data())

                for peer_info in response.get_data():
                    if peer_info.getId() == self._target_id:
                        self._finished = True
                        log.debug(f"{sender_info} sent {self._initiator.getId()} {self._targetid}")
                        targets_closest = RPCResponse(await self._protocol.try_find_close_nodes(\
                                                    self._initiator, self._initiator.getId(), self._target_id))
                         # check if the target node responded, if not just pass the k closest we have found already
                        if targets_closest.has_happened():              
                            self._shortlist.push_all(target_closest.get_data())
                            return (self._finished, merge_heaps(self._shortlist, self._contacted, self._k_val))
                        else:
                            log.warning(f"{self._target_id} did not respond")
                            return (False, merge_heaps(self._shortlist, self._contacted, self._k_val))
        # we failed ~(`-.-`)~ 
        if not finished and self._contacted.size() >= self._k_val and self._shortlist.size() == 0:
            return (False, merge_heaps(self._shortlist, self._contacted, self._k_val))
        else:
            return None



class KademliaValueSearch(KademliaSearch):
    """
    Finds a node with the value matching the key and returns the value. Also performs 
    iterative store by storing the value on the node on the closest neighbour that 
    didn't return the value.

    Attributes
    ----------
    _iterative_target : :class: `Node`
        The candidate for the iterative store.
    """


    def __init__(self, initiator, protocol, target_id, contacts, k=p.params['k'], alpha=p.params['alpha']):
        KademliaSearch.__init__(self, initiator, protocol, target_id, contacts, k, alpha)
        """
        """
        self._iterative_store_candidates = ContactHeap(target_id, k)
        """
        """


    async def search(self, rpc_method):
        """
        The public method for calling the the underlying kademlia search. 
        
        Parameters
        ----------
        rpc_method : :class: `rpc_protocol_method`
            The method used to find nodes.
        """
        return await self._search(rpc_method)



    async def _handle_responses(self, responses_to_handle):
        """
        Handles the response of the rpc_find_value calls. Upon completion performs an 
        iterative store on the value and the closest node that did not send us the value.
        Returns the success and either a list of k closest nodes to the key or the value that
        matches the key.

        Parameters
        ----------
        responses : list

        Returns
        -------
        (success, data) : tuple
            Whether the search was succesful and either the value if it was 
            found or a list of k closest nodes if the value was not found.
        """
        values_found = []

        for sender_info, response in responses_to_handle:
            response = RPCValueResponse(response)
            del(self._active_queries[sender_info])

            if response.has_happened():
                self._contacted.push(sender_info)

                if response.found_value():
                    values_found.append(response.get_data())
                    log.debug(f"(success) {sender_info} sent {self._initiator.getId()} {self._targetid}:{resonse.get_data()}")
                else:
                    # TODO
                    self._shortlist.push_all(response.get_data())
                    self._iterative_store_candidates.push(sender_info)
        # if the value is found perform an iterative store if possible and return the value
        if values_found:
            value = values_found[0]
            self._finished = True
            istore_target = None
            while self._iterative_store_candidates.size() > 0:
                # perform iterative store until it is successful
                istore_target = self._iterative_store_candidates.pop()
                log.debug(f"performing iterative store on {istore_target}")
                response = RPCValueResponse(await self._protocol.try_store_value(istore_target, self._target_id, value))
                # checking if store was successful
                if not response.has_happened():
                    log.warning(f"{self._initiator.getId()}'s iterative store failed because {istore_target} did not respond")
                else:
                    log.info(f"{istore_target} stored {value}")
                    return (self._finished, value)  
            log.warning(f"{self._initiator.getId()}'s iterative store failed because either no nodes to store on or\
                            no nodes responded")
            return(True, value)
        
        # search failed
        if not self._finished and (self._contacted.size() >= self._k_val or not self._shortlist.size() > 0):
            return (False, merge_heaps(self._contacted, self._shortlist, self._k_val))
        # continue
        return None



class KademliaStoreSearch(KademliaSearch):
    """
    Does a Node Search but instead of returning all nodes it sends a store rpc to each node with 
    the given data.

    Parameters:
    key : int
        The key of the data.
    value : str
        The data itself.
    """


    def __init__(self, initiator, protocol, target_id, value, contacts, k=p.params['k'], alpha=p.params['alpha']):
        KademliaSearch.__init__(self, initiator, protocol, target_id, contacts, k, alpha)
        """
        """
        self._key = target_id
        """
        """
        self._value = value
        """
        """


    async def search(self, rpc_method):
        """
        The public method for calling the underlying kademlia search.
        """
        return await self._search(rpc_method)


    async def _handle_responses(self, responses_to_handle):
        """
        Handles a dictionary of responses. On completion returns a tuple of if the node
        was found and a list of responses generated by calling a store rpc on the k closest 
        nodes found.

        Parameters
        ----------
        responses : :class: `RPCResponse`


        Returns
        ------
        (found, responses_to_handle) : tuple
        search_in_progress : boolean
        """ 
        for sender_info, response in responses_to_handle:
            log.info(f"processing {sender_info.getId()}'s data in {self._initiator.getId()}'s search")
            response = RPCResponse(response)
            del(self._active_queries[sender_info])
            
            if response.has_happened():
                self._contacted.push(sender_info)
                self._shortlist.push_all(response.get_data())

                for peer_info in response.get_data():
                    if peer_info.getId() == self._target_id:
                        log.debug(f"{sender_info} sent {self._initiator.getId()} {self._targetid}")
                        self._finished = True
                        target_closest = RPCResponse(await self._protocol.try_find_close_nodes(\
                                                    self._initiator,self._initiator.getId(), self._target_id))
                        if target_closest.has_happened():
                            self._shortlist.push_all(target_closest.get_data())
                            closest_contacts = merge_heaps(self._shortlist, self._contacted, self._k_val)
                            log.debug(f"(success) {self._target_id} sending store requests to {closest_contacts}")

                            active_queries = {}
                            for peer_contact in closest_contacts:
                                active_queries[peer.getId()] = self._protocol.try_store_value(peer_contact, self._key, self._value)
                            responses = await gather_responses(active_queries)

                            return (True, responses)
                        else:
                            log.warning(f"{self._target_id} did not respond in {self.initiator.getId()}\
                             StoreSearch. StoreSearch failed.")
                            return (False, None)
        # we failed ~(`-.-`)~ 
        if not self._finished and (self._contacted.size() >= self._k_val or not self._shortlist.size() > 0):
            closest_contacts = merge_heaps(self._shortlist, self._contacted, self._k_val)
            log.debug(f"(failure) {self._target_id} sending store requests to {closest_contacts}")
            active_queries = {}
            for peer_contact in closest_contacts:
                active_queries[peer_contact.getId()] = self._protocol.try_store_value(peer_contact, self._key, self._value)
            responses = await gather_responses(active_queries)
            return (True, responses)
        else:
            return None



class RPCResponse():
    """
    A wrapper class for managing the data of the responses in the rpc protocol.

    Parameters
    ----------
    response : list 
        A list of the success/failure of the response and the data received.
    """ 
    def __init__(self, response):
        self._happened = response[0]
        if isinstance(response[1], str):
            self._data = response[1]
        elif isinstance(response[1], list):
            print(response[1])
            self._data = [ tuple_to_contact(x) for x in response[1][1:] ]


    def tuple_to_contact(self, tuple):
        return Contact(tuple[0], tuple[1], tuple[2])


    def has_happened(self):
        """
        Returns true if there was a response, false otherwise.
        """
        return self._happened


    def get_data(self):
        """
        Gets the data in the response.
        """
        return self._data



class RPCValueResponse(RPCResponse):
    """
    A wrapper for a response from an rpc_find_value call. Adds a found_value method
    that checks if a value is in the response to the RPCResponse.
    """
    def __init__(self, response):
        RPCResponse.__init__(self, response)
        """
        """


    def found_value(self):
        """
        Checks if the data received is a list of contacts or some values
        """
        return this._happened and isinstance(str, self._data)


def tuple_to_contact(tuple):
    return Contact(tuple[0], tuple[1], tuple[2])
