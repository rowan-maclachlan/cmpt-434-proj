class Contact(object):
    """ 
    class::Contact
    A triple of a (big endian) node ID, host, and port for the host.
    This is the bare minimum of information needed to find another host on the
    network.
    """

    def __init__(self, id, host, port):
        """
        id : str
            The hash id of the contact
        host : str
            the hostname of the contact
        port : str
            The port that the host listens on
        """

        _dict = {}
        _dict['id'] = id
        _dict['host'] = host
        _dict['port'] = port


    def __str__(self):
        return "(" + str(id) + "/" + str(host) + "/" + str(port) + ")"

    def __repr__(self):
        return str(_dict)
