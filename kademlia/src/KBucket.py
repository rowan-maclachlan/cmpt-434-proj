from collections import deque

class KBucket(object):
    """ 
    class::KBucket
    Holds Contact elements.  This bucket is initialized with its maximum
    length.
    """

    def __init__(self, k):
        """
        Parameters
        ----------
        k : int 
            The maximum number of elements in this bucket.
        """
        _k = k
        contacts = deque(_k)
    
    def full(self):
        """
        Return true if this bucket is at capacity.
        """
        return True if len(contacts) >= contacts.maxlen else False


    def add(self, contact):
        """
        Add a contact to this bucket.  According to the specifications buckets
        should be ordered by least recently seen, except nodes are usually
        pinged to ensure they are still active.  We will just implement LRU for
        now, and kick out old contacts.

        Parameters
        ----------
        contact : Contact
            The contact to add to the bucket
        Return
        ------
        boolean : True if the contact was added to the bucket, and false
            otherwise.
        """
        if contact in contacts:
            # If this contact already appears in the list, move it to the back
            # of the list
            contacts.remove(contact)
            contacts.append(contact)
        elif not self.full():
            # If the contact doesn't appear in the list, append it.
            contacts.append(contact)
        else:
            # If the list is full, remove the oldest contact before appending
            # the new one.
            contacts.popleft()
            contacts.append(contact)
        return True


    def getSorted(self):
        """
        Get a copy of this buckets entries in sorted order
        """
        return sorted(contacts)
