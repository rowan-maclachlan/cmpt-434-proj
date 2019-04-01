import sys
import logging

from kademlia.Node import Node
from kademlia.utils import gather_responses
import kademlia.params as p

log = logging.getLogger(__name__)


class KademliaSearch():
	"""
	The search function used by Kademlia to find nodes in a Kademlia network.
	Asks the alpha closest nodes for their k closests nodes and then from
	the received nodes asks the alpha closest nodes for their k closests nodes
	iteratively until either no closer node is found or the node is found.
	The other classes in this file will define what it returned.

	Parameters
	----------
	initiator : :class:  `Node`
		The node that initaited the search.
	protocol : :class: `Protocol`
		The protocol used for finding nodes. 
	target_id : intorsomething
		The id of the node being searched for.
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

	def __init__(self, initiator, protocol, target_id, k=p.params['k'], alpha=p.params['alpha']):
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
		self._shortlist.push_all(self.initiator.find_nearest_neightbours(target_id))
		log.debug(f"Creating search with peers: {self._shortlist}")
		"""
		"""
		self._k_val = k
		"""
		"""
		self._alpha = alpha
		"""
		"""
		self._closest_node = self._shortlist.peekFirst()
		"""
		"""
		self._contacted = ContactHeap(target_id, k)
		"""
		"""
		self._active_queries = {}
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
		finished = False

		# loop until we have found the node, we have queried k nodes or all
		# responses returned were not closer then our closest yet
		while not finished and (self._contaced.size() <= self._k_val)\
							 and (prev_closest_node is not self._closest_node):
			prev_closest_node = self._closest_node
			
			peers_to_contact = []
			for i in range(self._alpha):
				peers_to_contact.append(self._shortlist.pop())

			for peer in peers_to_contact:
				self._active_queries[peer.getId()] = rpc_method(self._initiator, peer) 

			responses = await gather_responses(self._response_dict)
			# handles the responses, may terminate the search by setting finished to true,
			# expanding contacted to be greater than k, or determining no nodes found are
			# closer than the closest we have found so far
			result = await self._handle_responses(responses)

		return result




class KademliaNodeSearch(KademliaSearch):
	"""
	Does a node search, returning a tuple of the success of the search
	and the k closest nodes of the closest node to the target_key. This may be the
	node with the target_key if found or simply some close node. May return 
	fewer than k nodes if there are fewer than k nodes in the closest node's
	bucket.
	"""


	def __init__(self, initiator, protocol, target_id, k=p.params['k'], alpha=p.params['alpha']):
		KademliaSearch.__init__(self, initiator, protocol, target_id, k, alpha)


	async def search(self, rpc_method):
		"""
		Calls the basic kademlia search
		"""
		return await self._search(rpc_method)


	async def _handle_responses(self, responses_to_handle):
		"""
		Handles a dictionary of responses. On completion returns a tuple of the success
		of the search and either the target_id's contact information or returns the closest
		node to the target_id's contact information. If the search will continue, returns 
		only True.

		Parameters
		----------
		responses : :class: `RPCResponse`


		Returns
		------
		(successful, contact_info) : tuple
		search_in_progress : boolean
		""" 
		newly_contacted = []

		for sender_info, response in responses_to_handle:
			log.debug(f"processing {sender_info.getId()}'s data in {self._initiator.getId()}'s search")
			
			if response.has_happened():
				newly_contacted.append(sender_info)
				self._shortlist.push_all(response.get_data())

				for peer_info in response.get_data():
					# for now not making sure they are active, if I can learn about how
					# to send pings and not have to await their finishing I'll think 
					# about adding an active list
					if peer_info.getId() == self._target_id:
						finished = True

						target_closest = await self._protocol.find_close_nodes(self._initiator, self._initiator.getId(), self._target_id)
						self._shortlist.push_all(target_closest)

						return (finished, merge_heaps(self._shortlist, self._contacted))

		self._contacted.push_all(newly_contacted)

		any_closer = distance_to(self._target_id, self._closest_node.getId())\
					 >= distance_to(self._target_id, self._shortlist.peekFirst())

		# we failed ~(`-.-`)~ 
		#TODO: what to return on failure
		if not finished and (self._contacted.size() >= self._k_val or not any_closer):
			return (finished, merge_heaps(self._shortlist, self._contacted))
		else:
			self._closest_node = self._shortlist.peekFirst()
			return True



class KademliaValueSearch(KademliaSearch):
	"""
	Finds a node with a value and returns that node. Also performs iterative storing
	by storing the value on the node on the closest neighbour that didn't return the 
	value.

	Attributes
	----------
	_iterative_target : :class: `Node`
		The candidate for the iterative store.
	"""

	def __init__(self, initiator, protocol, target_id, k=p.params['k'], alpha=p.params['alpha']):
		KademliaSearch.__init__(self, initiator, protocol, target_id, k, alpha)
		"""
		"""
		self._iterative_target
		"""
		"""


	def search(self, rpc_method):
		"""
		Calls the the underlying kademlia search.
		
		Parameters
		----------
		rpc_method : :class: `rpc_protocol_method`
			The method used to find nodes.
		"""
		self._search(rpc_method)



	def _handle_responses(self, responses):
		"""

		"""




class RPCResponse():
    """
    A wrapper class for managing the data of the responses in the protocol.

    Parameters
    ----------
    response : tuple
 		A tuple of the success/failer of the response and the data received.
    """ 
    def __init__(self, response):
        self._response = response
        """
        """


    def has_happened(self):
        """
        Returns if the response happend or timed out.
        """
        return self._response[0]


    def get_data(self):
        """
        Gets the data in the response.
        """
        return self._response[1].values()