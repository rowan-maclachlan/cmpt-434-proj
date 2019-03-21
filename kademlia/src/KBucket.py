import params as p
import Contact

class KBucket:
    """ 
    class::Bucket
    """

    def __init__(self, b, k):
        """
        b : int
            The number of bucket bits.
        k : int 
            The number of entries per bucket
        """
        _b = b
        _k = k
        _buckets = [[] for i in range(b)]

    def add_contact(self, bucket, contact):
        """
        Add the contact to the bucket.

        bucket : int
            The number of the bucket we are adding the contact to.
        contact : Contact
            The contact we wish to add.

        bool
            Return true if the contact was added to the bucket, and false
            otherwise.
        """
        # If the bucket is full, do nothing
        if len(_buckets[bucket]) >= p.params[K]:
            # TODO implement replacement algorithm
            print("Throwing away " + str(contact))
        else:
            _buckets[bucket].prepend(contact)

