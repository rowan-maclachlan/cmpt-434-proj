import params as p
import Contact
import logging as l

class KBucket(object):
    """ 
    class::KBucket
    Hold a p.params[B] buckets.  Each bucket has a max length of p.params[K].
    The contents of a bucket are class::Contact.
    """

    def __init__(self, b, k, id):
        """
        b : int
            The number of bucket bits.
        k : int 
            The number of entries per bucket
        id : int
            The ID of the Node that has this KBucket
        """
        _b = b
        _k = k
        _id = id
        _buckets = [[] for i in range(b)]


    def add_contact(self, contact):
        """
        Add the contact to the bucket.  The bucket we add the contact to is
        determined by their largest differing bit from ours.

        contact : Contact
            The contact we wish to add.

        bool
            Return true if the contact was added to the bucket, and false
            otherwise.
        """
        id = contact.getId()
        if id == _id:
            l.debug("Failed to add ID {} to bucket: cannot add self to bucket".format(id))
            return false
            
        index = _get_bucket_index(id)
        # If the bucket is full, do nothing
        if len(_buckets[index]) >= p.params[K]:
            # TODO implement proper replacement algorithm
            l.info("Throwing away contact with ID {}.".format(id))
        else:
            # TODO implement proper replacement algorithm
            _buckets[index].prepend(contact)


    def find_nearest_neighbour(self, id):
        """
        Find and return the K nearest Contacts to the id provide, excluding
        the ID of this K bucket owner.
        id : int
            The digest value for which we want to find the k nearest neighbours
        """
        # TODO implement!
        return [ Contact(None, None, None) for x in range(_k) ]


    def _get_bucket_index(self, id):
        # TODO Can this be implemented better?
        # Calculate the XOR distance of this bucket with the ID
        distance = id ^ _id
        bit = 0
        while distance > 0:
            # Count the index of the largest bit in the distance
            # The distance will be zero after 'bit' many shifts.
            distance = distance >> 1
            bit += 1

        return bit
