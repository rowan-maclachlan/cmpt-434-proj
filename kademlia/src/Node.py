import params as p
import hashing as hashing
import Bucket

class Node:
    """ 
    class::Node
    """

    def __init__(self, host, port):
        """
        host : str
            The hostname this node resides on
        port : str
            The port this node will listen for connections on
        """
        _me = Contact(hashing.new_id(host, port), host, port)
        _bucket = KBucket(p.params[B], p.params[K])
