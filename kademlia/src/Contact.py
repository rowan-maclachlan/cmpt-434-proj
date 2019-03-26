class Contact(object):
    """ 
    class::Contact
    A triple of a (big endian) node ID, host, and port for the host.
    This is the bare minimum of information needed to find another host on the
    network.
    """
    def __init__(self, id, ip, port):
        """
        id : str
            The hash id of the contact
        ip : str
            the ip of the contact
        port : str
            The port that the host listens on
        """

        _dict = {}
        _dict['id'] = id if id is not None else "UNKNOWN"
        _dict['ip'] = ip
        _dict['port'] = port


    def getId(self):
        return self._dict['id']


    def getIp(self):
        return self._dict['ip']


    def getPort(self):
        return self._dict['port']


    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self._id == other._id and \
               self._ip == other._ip and \
               self._port == other._port


    def __hash__(self):
        return hash((self._id, self._ip, self._port))


    def __str__(self):
        return "(" + str(self._id) + "/" + str(self._ip) + "/" + str(self._port) + ")"


    def __repr__(self):
        return str(_dict)
