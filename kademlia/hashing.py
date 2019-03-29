import hashlib
import kademlia.params as p 
import random # For random ID generation

"""
See https://docs.python.org/3/library/hashlib.html on hashing in Python
"""

def get_mask():
    """
    Get a mask of B bits.
    """
    return (1 << p.params[p.B]) - 1

def hash_function(data):
    """
    Hash the data to a byte array of length p.params[B] / 8

    data : binary data
    
    int 
        A hash of length p.params[B] / 8 in hexadecimal string form.
    """
        
    return int(hashlib.sha1(data.encode()).hexdigest(), 16) & get_mask() 

def new_id(host, port):
    """ 
    Create a new Node hash ID by hashing host and port.

    host : str
        The Node hostname
    port : str
        The Node port number that it listens on

    str 
        A hash of length p.params[B] / 8 in hexadecimal string form.
    """
    return int(hashlib.sha1((host + port).encode()).hexdigest(), 16) & get_mask()

def new_id():
    """ 
    Create a random new Node ID.

    str 
        A hash of length p.params[B] / 8 in hexadecimal string form.
    """
    return random.randint(0, get_mask())

