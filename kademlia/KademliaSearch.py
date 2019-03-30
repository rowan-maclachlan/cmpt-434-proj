import sys
import logging

from kademlia.Node import Node


log = logging.getLogger(__name__)

Class KademliaSearch():
	"""
	The search function used by Kademlia to find nodes in a Kademlia network.
	Asks the alpha closest nodes for their k closests nodes and then from
	the received nodes asks the alpha closest nodes for their k closests nodes
	iteratively until either no closer node is found or the node is found.

	Parameters
	----------
	initiator : :class:  `Node`
		The node that initaited the search.
	protocol : :class: `Protocol`
		The protocol that will be used to query other nodes for info on
		their closest nodes. Needs an implementation rpc_find_closest_neighbours.
	target_id : intorsomething
		The id of the node being searched for.

	Attributes
	----------
	_initiator : :class:  `Node`
		The node that initaited the search.
	_protocol : :class: `Protocol`
		The protocol that will be used to query other nodes for info on
		their closest nodes. Needs an implementation rpc_find_closest_neighbours.
	_target_id : intorsomething
		The id of the node being searched for.
	_shortlist : list
		The list of nodes to be queried for their closest neighbours.
	_closest_node : :class: `Node`
		The closest node found so far in this search.
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
		self._shortlist = ContactHeap(self._initiator.me['id'])
		log.debug(f"Creating search with peers: {self._shortlist}")
		"""
		"""
		self._closest_node = initiator
		"""
		"""


	async def _search(self, rpc_method):
		"""
		The base level search that takes place in any of the possible searches in a 
		Kademlia network. This retrives the k closest nodes from the alpha closest neighbours.

		Parameters
		----------
		rpc_method : :class: `Protocol`
			The rpc function that defines the result of the queries of nodes. Used to query
			the nodes.
		""" 
		prev_closest_node = self._closest_node

		# set up the shortlist


