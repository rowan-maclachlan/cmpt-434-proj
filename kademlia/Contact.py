import kademlia.hashing as h

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
