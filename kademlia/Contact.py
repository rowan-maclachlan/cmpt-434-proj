import logging
import heapq

import kademlia.hashing as h
import kademlia.params as p
from kademlia.utils import distance_to

log = logging.getLogger(__name__)


class Contact():
    """ 
    A triple of a (big endian) node ID, host, and port for the host.
    This is the bare minimum of information needed to find another host on the
    network.

    Parameters
    ----------
    id : int 
        The hash id of the contact.  If the ID is none, a random hash is
        created.
    ip : str
        the ip of the contact
    port : str
        The port that the host listens on
    """

    def __init__(self, id, ip, port):
        if id is None:
            id = h.new_id() 
        self._id = id
        self._ip = ip
        self._port = port


    def getId(self):
        return self._id


    def getIp(self):
        return self._ip


    def getPort(self):
        return self._port


    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
                self.getId() == other.getId()

    def __ne__(self, other):
        return isinstance(other, self.__class__) and \
                self.getId() != other.getId()

    def __lt__(self, other):
        return isinstance(other, self.__class__) and \
                (self.getId() < other.getId())

    def __le__(self, other):
        return isinstance(other, self.__class__) and \
                (self.getId() <= other.getId())

    def __gt__(self, other):
        return isinstance(other, self.__class__) and \
                (self.getId() > other.getId())

    def __ge__(self, other):
        return isinstance(other, self.__class__) and \
                (self.getId() >= other.getId())

    def __hash__(self):
        return self.getId()


    def __iter__(self):
        return iter([self._id, self._ip, self._port])


    def __str__(self):
        return f"({self.getId()},{self.getIp()},{self.getPort()})"


    def __repr__(self):
        return str(self)


class ContactHeap():
    """
    A data class for storing a heap of contacts. Sorted by the contact's xor distance to
    the given node. Note PLEASE: the real heap size can grow to be larger than maxsize but only
    maxsize of the elements will be visible to any function calling from the outside.

    Parameters
    ----------
    node_id : int
        The id who distance from determines the heap order.
    maxsize : int
        The maximum size the heap can become. Defualt value is K

    Attributes
    ----------
    _node_id : int
        The id who's distance to the other node_ids defines the heap order.
    _maxsize : int
        The maximum size of the heap.
    _heap : list
        The heap of contacts.
    _contacted : set
        The set of nodes that have already been contacted.
    _node_dict : dict
        A dictionary of all nodes in the heap used for fast checking if a node 
        is already in the heap.
    """

    def __init__(self, node_id, maxsize=p.params['k']):
        self._node_id = node_id
        """
        """
        self._maxsize = maxsize
        """
        """
        self._heap = []
        """
        """
        self._node_dict = {}
        """
        """


    def remove(self, contacts):
        """
        Removes the given contacts from the heap. Contacts can be a single contact or many.
        Since the heap's real size can be larger than the maxsize, removing nodes may
        not actually change he heap's visible size as nodes not visible previously can
        fill the empty spots.

        Parameters
        ----------
        contacts : list
            The contacts to remove from the heap
        """
        if not contacts:
            return

        new_heap = []

        for ell in self._heap:
            if ell not in contacts: 
                distance = distance_to(self._node_id, ell.getId())
                heapq.heappush(new_heap, (distance, ell))

        self._heap = new_heap


    def push(self, contact):
        """
        Pushes the given contact onto the heap as long as the contact isn't the one 
        for the reference node_id or already in the heap.

        Parameters
        ----------
        contact : :class: `Contact`
            The contact to add.
        """
        if not contact or contact.getId() == self._node_id:
            return

        # if the node is already in the heap don't add it
        if self.contains(contact):
            return
        else:
            distance = distance_to(self._node_id, contact.getId())
            heapq.heappush(self._heap, (distance, contact))
            self._node_dict[contact.getId()] = contact


    def push_all(self, contacts):
        """
        Adds a list of contacts to the given heap.

        Parameters
        ----------
        contacts : list
            The list of contacts to be added.
        """
        for ell in contacts:
            self.push(ell)


    def pop(self):
        """
        Pops a contact from the heap, removes it from the node dictionary, and
        returns it.

        Return
        ------
        :class: `Contact` : the popped contact
        """
        if not self._heap:
            log.debug("popped from empty heap")
            return

        popped_contact = heapq.heappop(self._heap)[1]
        del self._node_dict[popped_contact.getId()]

        return popped_contact


    def peek_first(self):
        """
        Gets the contact at the top of the heap without popping it off the
        heap. Note: unlike pop, which only returns the contact, this gives the tuple
        of (distance, contact) so that comparisons can be made more easily.

        Return
        ------
        tuple : the distance and the closest contact to the node id
        """
        return self._heap[0]


    def contains(self, contact):
        """
        Checks if the heap contains a contact.

        Parameters
        ----------
        contact : :class: `Contact`
            Is this contact in the heap?

        Returns
        -------
        isIn : boolean
        """
        if contact.getId() in self._node_dict.keys():
            return True
        else:
            return False

    
    def size(self):
        """
        Gets the number of ellements in the heap.

        Returns
        -------
        numEll : int
        """
        return len(self._heap)


    def get_heap(self):
        """
        Gets the heap.

        Returns
        -------
        contact_heap : heap
        """
        return self._heap
