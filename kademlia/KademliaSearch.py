import sys
import logging

from kademlia.Node import Node


Class KademliaSearch():
	"""
	The search function used by Kademlia to find nodes in a Kademlia network.
	Asks the alpha closest nodes for their k closests nodes and then from
	the received nodes asks the alpha closest nodes for their k closests nodes
	iteratively until either no closer node is found or the node is found.

	Attributes
	----------
	_initiator : :class:  `Node`
		The node that initaited the search.
	_protocol : :class: `Protocol`
		The protocol that will be used to query other nodes for info on
		their closest nodes. Needs an implementation rpc_find_closest_neighbours.
	_target_node : :class: `Node`
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
		self._shortlist = None
		"""
		"""
		self._closest_node = None
