import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
import pytest

from kademlia.KBucket import KBucket
from kademlia.Contact import Contact
import kademlia.params as p 

def test_kbucket_add_same_contact():
    b = p.params[p.B]
    k = p.params[p.K]
    ip = "127.0.0.1"
    port = 1234

    contact = Contact(None, ip, port)
    kbucket = KBucket(k)

    assert kbucket.add(contact)
    assert len(kbucket) == 1

    assert kbucket.add(contact)
    assert len(kbucket) == 1

    assert contact in kbucket 


def test_kbucket_len():
    b = p.params[p.B]
    k = p.params[p.K]
    ip = "127.0.0.1"
    port = 1234

    contact1 = Contact(None, ip, port)
    contact2 = Contact(None, ip, port)
    contact3 = Contact(None, ip, port)
    kbucket = KBucket(k)

    assert len(kbucket) == 0
    assert kbucket.add(contact1)
    assert len(kbucket) == 1
    assert kbucket.add(contact2)
    assert len(kbucket) == 2
    assert kbucket.add(contact3)
    assert len(kbucket) == 3

test_kbucket_add_same_contact()
test_kbucket_len()