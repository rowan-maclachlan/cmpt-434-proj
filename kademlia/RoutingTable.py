import params as p
import Contact
import logging

log = logging.getLogger(__name__)

class RoutingTable(object):
    """ 
    class::RoutingTable
    Hold a p.params[B] KBuckets.  Each bucket has a max length of p.params[K].
    The contents of a bucket are class::Contact.
    """

    def __init__(self, b, k, id):
        """
        b : int
            The number of bucket bits.
        k : int 
            The number of entries per bucket
        id : int
            The ID of the Node that has this Routing Table 
        """
        b = b
        k = k
        id = id
        buckets = [ KBucket(k) for _ in range(b) ]

    
    def __contains__(self, contact):
        """
        Check if this routing table contains an entry for the contact.

        Parameters
        ----------
        contact : Contact
            The contact to look for

        Return
        ------
        boolean : True if this routing table contains an entry for the contact,
                  and False otherwise.
        """
        return contact in _get_bucket(contact.getId())

    def add_contact(self, contact):
        """
        Add the contact to the routing table.

        Parameters
        ----------
        contact : Contact
            The contact we wish to add.

        Return
        ------
        bool
            Return True if the contact was added to the routing table, and
            False otherwise.
        """
        id = contact.getId()
        if id == self.id:
            l.error(f"Failed to add ID {id} to bucket: can't add self to bucket")
            return False

        l.debug(f"Adding contact {id} to this routing table.")
            
        return _get_bucket(id).add(contact)


    def remove_contact(self, contact):
        """
        Remove the contact from the routing table.

        Parameters
        ----------
        contact : Contact
            The contact we wish to remove

        Return
        ------
        bool
            Return True if the contact was removed from the routing table, and
            False if the contact was not present in the table.
        """
        l.debug(f"Removing contact {contact.getId()} from this routing table.")
            
        return _get_bucket(id).remove(contact)


    def find_nearest_neighbours(self, id):
        """
        Find and return the K nearest Contacts to the ID provided.  Sort all
        the contact bucket entries according to distance from the provided ID,
        and return the first K contacts in that result.  Could probably be made
        more efficient.

        Parameters
        ----------
        id : int
            The digest value for which we want to find the k nearest neighbours

        Return
        ------
        [Contact] : A list of Contacts.  These are the K nearest contacts in this
        routing table to the ID provided.
        """
        # TODO improve?
        # collect all bucket entries, sort all bucket entries
        nearest_neighbours = []
        # flatten all contacts into one list
        all_contacts = [ el for lst in self.buckets for el in lst.getSorted() ]
        # sort contacts according to distance from ID
        sorted_contacts = sorted(all_contact, key=(lambda x: x.getId() ^ id))
        
        return sorted_contacts[:self.k]


    def _get_bucket(self, id):
        # TODO Can this be implemented better?
        # TODO If an id is different only in the least significant bit, does it
        # belong in bucket [0] or bucket[1]?  This assumes bucket[0] because
        # there's no need for a bucket of this table's node and there wouldn't
        # be room for the furthest away bucket if there was.
        # Calculate the XOR distance of this bucket with the ID
        distance = id ^ self.id
        index = 0
        while distance > 1:
            # Count the index of the largest bit in the distance
            # The distance will be zero after 'bit' many shifts.
            distance = distance >> 1
            index += 1

        return self.buckets[index]
