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
        while not self._finished :
            peers_to_contact = []
            # If the closest node we found is farther away than our current
            # closest node, query the next k closest nodes
            if (distance_to(self._target_id, self._closest_node.getId())\
                    >= distance_to(self._target_id, self._shortlist.peek_first()[1].getId())):
                self._closest_node = self._shortlist.peek_first()[1]

                peers_to_contact.extend(self._shortlist.pop_all(self._alpha))
            else:
                # if there are no closer nodes we search the nearest k nodes instead of a
                # the nearest alpha 
                log.debug("No longer finding closer nodes than before...")
                peers_to_contact.extend(self._shortlist.pop_all(self._k_val))
            log.debug(f"{self._initiator} preparing to contact: {peers_to_contact}")
            for peer in peers_to_contact:
                self._active_queries[peer] = rpc_method(peer, self._target_id) 
            responses = await gather_responses(self._active_queries)
            # handles the responses. May terminate the search by setting finished to true,
            # expanding contacted to be greater than k, or determining no nodes found are
            # closer than the closest we have found so far
            result = await self._handle_responses(responses)
            prev_closest_node = self._closest_node

        # ( boolean, str or list[Contacts] )
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
            del(self._active_queries[sender_info])

            if response.has_happened():
                self._contacted.push(sender_info)

                for peer_info in response.get_data():
                    # If we found ourselves, set finished to true.  Then, we
                    # process the other reponses
                    if peer_info.getId() == self._target_id:
                        log.debug(f"Found target {self._target_id} in contact {sender_info}")
                        self._finished = True
                    else:
                        # push peer info onto contact heap if it has not been contacted, continue to process
                        # responses
                        if peer_info.getId() in self._contacted:
                            self._shortlist.push(peer_info)
        # we failed ~(`-.-`)~ 
        if self._finished:
            return (True, merge_heaps(self._shortlist, self._contacted, self._k_val))
        elif len(self._contacted) >= self._k_val or not len(self._shortlist) > 0:
            self._finished = True
            return (False, merge_heaps(self._shortlist, self._contacted, self._k_val))
        else:
            return (False, [])



class KademliaValueSearch(KademliaSearch):
    """
    Finds a node with the value matching the key and returns the value. Also performs 
    iterative store by storing the value on the node on the closest neighbour that 
    didn't return the value.

    Attributes
    ----------
    _iterative_store_candidates : :class: `Node`
        The candidates for an iterative store.
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
                    log.debug(f"(success) {sender_info} sent {self._initiator.getId()} {self._target_id}:{response.get_data()}")
                else:
                    self._shortlist.push_all(response.get_data())
                    self._iterative_store_candidates.push(sender_info)
        # If the value is returned by a node, an iterative store should take place from
        # choosing the closest node that has not returned a value to us. i.e. the closest
        # node to the node that has the key:value pair that we know doesn't have the key:value
        # pair stored already.
        value = None
        if values_found:
            value = values_found[0]
            self._finished = True
            istore_target = self._iterative_store_candidates.pop()
            # make sure there is actually a candidate for the iterative store first
            if not istore_target == None:
                log.debug(f"{self._initiator.getId()} performing iterative store on {istore_target}")
                istore = RPCValueResponse(await self._protocol.try_store_value(istore_target, self._target_id, value))
                if istore.has_happened():
                    log.info(f"{istore_target} stored {value}")
                else:
                    log.error(f"iterative store {istore_target.getId()} failed due to timemout")
        # the search was successful, return the value
        if self._finished:
            return (True, value)    
        # search finished but did not find the value, returns k closest contacts
        # to the key given
        if len(self._contacted) >= self._k_val or not len(self._shortlist) > 0:
            self._finished = True
            return (False, merge_heaps(self._contacted, self._shortlist, self._k_val))
        # continue the search
        return (False, [])



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
                # Check each respoonse to see if it is the target_id. If it is not
                # then it gets added to the shortlist.
                for peer_info in response.get_data():
                    if peer_info.getId() == self._target_id:
                        self._finished = True
                    else:
                        if not peer_info in self._contacted:
                            self._shortlist.push(peer_info)
        # Whether the search completes or the node is found the resulting actions
        # are the same: a store is performed using the value passed in on the k-closest
        # nodes that have been found.
        if self._finished or len(self._contacted) >= self._k_val or not len(self._shortlist) > 0:
            # Because this flag is used to exit the search and could not have been set
            # if we didn't find the target id, it must be set here
            self._finished = True
            closest_contacts = merge_heaps(self._shortlist, self._contacted, self._k_val)
            log.debug(f"{self._target_id} sending store requests to {closest_contacts}")
            active_queries = {}
            for peer_contact in closest_contacts:
                active_queries[peer_contact.getId()] = self._protocol.try_store_value(peer_contact, self._key, self._value)
            await gather_responses(active_queries)
            return (True, )
        else:
            return (False, [])



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
            self._data = [ tuple_to_contact(x) for x in response[1][0:] ]


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
        return self._happened and isinstance( self._data, str)


def tuple_to_contact(tuple_info):
    print(tuple_info)
    return Contact(tuple_info[0], tuple_info[1], tuple_info[2])
