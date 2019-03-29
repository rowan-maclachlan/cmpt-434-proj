import sys
sys.path.append('/home/silentknight/School/CS434/434proj/cmpt-434-proj')

from collections import deque

class KBucket():
    """ 
    Holds :class:`Contact` elements.  This bucket is initialized with its
    maximum length, which should correspond to the value of :data:`params.K` in
    :mod:`params`.

    Parameters
    ----------
    k : int 
        The maximum number of elements in this bucket.
    """

    def __init__(self, k):
        self.k = k
        self.contacts = deque(maxlen=k)

    
    def __contains__(self, contact):
        """
        Check if this bucket contains an entry for the :class:`contact <Contact>`

        Parameters
        ----------
        contact : Contact
            The contact to look for

        Return
        ------
        boolean : True if this KBucket contains the contact, and False otherwise.
        """
        return contact in self.contacts 

    def __len__(self):
        return len(self.contacts)


    def full(self):
        """
        Return true if this bucket is at capacity.
        """
        return True if len(self.contacts) >= self.contacts.maxlen else False


    def add(self, contact):
        """
        Add a :class:`Contact` to this bucket.  According to the specifications buckets
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
        if contact in self.contacts:
            # If this contact already appears in the list, move it to the back
            # of the list
            self.contacts.remove(contact)
            self.contacts.append(contact)
        elif not self.full():
            # If the contact doesn't appear in the list, append it.
            self.contacts.append(contact)
        else:
            # If the list is full, remove the oldest contact before appending
            # the new one.
            self.contacts.popleft()
            self.contacts.append(contact)
        return True


    def remove(self, contact):
        """
        Remove a :class:`Contact` from this bucket.  According to the specifications, we
        should be replacing this contact from a full K bucket with a backup
        cache of active contacts.  Just kick it out for now.
    
        Parameters
        ----------
        contact : Contact
            The contact to remove from this bucket. 
        Return
        ------
        boolean : True if the contact was removed from the bucket, and false
            if they were not in it to begin with.
        """
        if contact in self.contacts:
            self.contacts.remove(contact)
            return True
        else:
            return False


    def getSorted(self):
        """
        Get a copy of this bucket's entries in sorted order
        """
        return sorted(self.contacts)


    def __str__(self):
        return str(self.contacts)
