import hashlib
import params as p
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

    TODO: How do we truncate this large integer?  mod?  or mask?
        what would we mod by?

    data : binary data
    
    int 
        A hash of length p.params[B] / 8 in hexadecimal string form.
    """
        
    return int(hashlib.sha1(data).hexdigest(), 16) & get_mask() 

def new_id(host, port):
    """ 
    Create a new Node hash ID by hashing.
    TODO: Does this need to be random or can it be based on node ID?  IP and
    port number?

    host : str
        The Node hostname
    port : str
        The Node port number that it listens on

    str 
        A hash of length p.params[B] / 8 in hexadecimal string form.
    """
    return int(hashlib.sha1(host + port).hexdigest(), 16) & get_mask()
