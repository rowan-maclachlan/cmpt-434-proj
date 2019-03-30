import kademlia.hashing as h
import params as p
from kademlia.utils import distance_to

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
        self._dict = {}
        if id is None:
            id = h.new_id() 
        self._dict['id'] = id
        self._dict['ip'] = ip
        self._dict['port'] = port


    def getId(self):
        return self._dict['id']


    def getIp(self):
        return self._dict['ip']


    def getPort(self):
        return self._dict['port']


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


    def __str__(self):
        return f"({self.getId()}/{self.getIp()}/{self.getPort()})"


    def __repr__(self):
        return str(self._dict)


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
    """

    __init__(self, node_id, maxsize=p.params['k']):
        self._node_id = node_id
        """
        """
        self._maxsize = maxsize
        """
        """
        self._heap = []
        """
        """
        self._contacted = Set()
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
                distance = distance_to(self._node_id, ell['id'])
                heapq.heappush(new_heap, (distance, ell))

        self._heap = new_heap


    def add(self, contacts):
        """
        Adds the given contacts to the heap. Contacts can be a single contact or many.
        
        """