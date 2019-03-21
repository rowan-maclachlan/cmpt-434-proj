"""
See https://docs.python.org/3/library/hashlib.html on hashing in Python
"""
import hashlib
import params as p

def hash_function(data):
    """
    Hash the data to a byte array of length p.params[B] / 8
    TODO: How do we draw this down to the length of B?

    data : str
    
    str 
        A hash of length p.params[B] / 8 in hexadecimal string form.
    """
    return hashlib.sha1(data).hexdigest()

def new_id(host, port):
    """ 
    Create a new Node hash ID by hashing.
    TODO: Does this need to be random or can it be based on node ID?

    host : str
        The Node hostname
    port : str
        The Node port number that it listens on

    str 
        A hash of length p.params[B] / 8 in hexadecimal string form.
    """
    return hashlib.sha1(host + port).hexdigest()
