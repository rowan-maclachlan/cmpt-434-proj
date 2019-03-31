import sys
import logging

from kademlia.Node import Node
import kademlia.params as p

log = logging.getLogger(__name__)

Class KademliaSearch():
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
	_closest_node : :class: `Node`
		The closest node found so far in this search.
	_response_dict : dict
		a dictionary of responses with keys of the sender's ID who gave the response and values as 
		the response
	""" 

	__init__(self, initiator, protocol, target_id):
		self._initiator = initiator
		"""	
		"""
		self._protocol = protocol
		"""
		"""
		self._target_id = target_id
		"""
		"""
		self._shortlist = ContactHeap(self._initiator.me.getId())
		self._shortlist.push_all(self.initiator.find_nearest_neightbours(target_id))
		log.debug(f"Creating search with peers: {self._shortlist}")
		"""
		"""
		self._alpha = p.params['alpha']
		"""
		"""
		self._closest_node = self._shortlist.peekFirst()
		"""
		"""
		self._contacted = set()
		"""
		"""
		self._response_dict = {}
		"""
		"""


	async def _search(self, rpc_method):
		"""
		The base level search that takes place in any of the possible searches in a 
		Kademlia network. This retrives the k closest nodes from the alpha closest neighbours.

		Parameters
		----------
		rpc_method : :class: `Protocol`
			The rpc function that defines the result of the queries of nodes. The function used 
			to query the nodes in the search.
		""" 
		prev_closest_node = None
		finished = False

		# loop until we have found the node, we have queried k nodes or all
		# responses returned were not closer then our closest yet
		while not finished and (self._contaced.size() <= p.params['k'])\
							 and (prev_closest_node is not self._closest_node):
			
			peers_to_contact = []
			for i in range(self._alpha):
				peers_to_contact.append(self._shortlist.pop())

			for peer in peers_to_contact:
				self._response_dict[peer.getId()] = rpc_method(self._initiator, peer) 

			responses = await gather_responses(self._response_dict)
			# handles the responses, may terminate the search by setting finished to true,
			# expanding contacted to be greater than k, or determining no nodes found are
			# closer than the closest we have found so far
			self._handle_responses(responses)

