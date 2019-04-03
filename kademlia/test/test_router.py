import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
import pytest

from kademlia.RoutingTable import RoutingTable
from kademlia.KBucket import KBucket
from kademlia.Contact import Contact
import kademlia.params as p 

def test_get_bucket():
    b = p.params[p.B]
    k = p.params[p.K]
    ip = "127.0.0.1"
    port = 1234

    contact1 = Contact(1, ip, port)
    contact2 = Contact(2, ip, port)
    contact3 = Contact(4, ip, port)
    contact4 = Contact(8, ip, port)

    table = RoutingTable(b, k, 0)

    assert table.add(contact1)
    assert contact1 in table
    assert len(table) == 1
    assert len(table.get_bucket(contact1.getId())) == 1

    assert table.add(contact2)
    assert contact2 in table
    assert len(table) == 2
    assert len(table.get_bucket(contact2.getId())) == 1

    assert table.add(contact3)
    assert contact3 in table
    assert len(table) == 3
    assert len(table.get_bucket(contact3.getId())) == 1

    assert table.add(contact4)
    assert contact4 in table
    assert len(table) == 4
    assert len(table.get_bucket(contact4.getId())) == 1


def test_wont_add_self():
    b = p.params[p.B]
    k = p.params[p.K]
    ip = "127.0.0.1"
    port = 1234

    contact = Contact(0, ip, port)
    
    table = RoutingTable(b, k, 0)

    assert not table.add(contact)
    assert contact not in table
    assert len(table) == 0


def test_add():
    b = p.params[p.B]
    k = p.params[p.K]
    ip = "127.0.0.1"
    port = 1234

    contact1 = Contact(None, ip, port)
    contact2 = Contact(None, ip, port)
    contact3 = Contact(None, ip, port)
    contact4 = Contact(None, ip, port)

    table = RoutingTable(b, k, 0)

    assert table.add(contact1)
    assert table.add(contact2)
    assert table.add(contact3)
    assert table.add(contact4)


def test_remove_contact():
    b = p.params[p.B]
    k = p.params[p.K]
    ip = "127.0.0.1"
    port = 1234

    contact1 = Contact(None, ip, port)
    contact2 = Contact(None, ip, port)
    contact3 = Contact(None, ip, port)
    contact4 = Contact(None, ip, port)

    table = RoutingTable(b, k, 0)

    assert table.add(contact1)
    assert table.add(contact2)
    assert table.add(contact3)
    assert table.add(contact4)

    assert table.remove(contact1)
    assert table.remove(contact2)
    assert table.remove(contact3)
    assert table.remove(contact4)
    assert not table.remove(contact4)


def test_find_nearest_neighbours():
    """
    Add 8 contacts to the routing table.
    Assert that when we call find nearest with some ID, we get 4 of those
    contacts which are nearest to the function's argument.
    """

    k = 4
    ip = "127.0.0.1"
    port = 1234

    contact1 = Contact(1, ip, port)
    contact2 = Contact(2, ip, port)
    contact3 = Contact(3, ip, port)
    contact4 = Contact(4, ip, port)
    contact5 = Contact(8, ip, port)
    contact6 = Contact(9, ip, port)
    contact7 = Contact(10, ip, port)
    contact8 = Contact(11, ip, port)

    table = RoutingTable(4, k, 0)

    assert table.add(contact1)
    assert table.add(contact2)
    assert table.add(contact3)
    assert table.add(contact4)
    assert table.add(contact5)
    assert table.add(contact6)
    assert table.add(contact7)
    assert table.add(contact8)

    nearest = table.find_nearest_neighbours(12)
    assert len(nearest) == 4

    assert contact8 in nearest
    assert contact7 in nearest
    assert contact6 in nearest
    assert contact5 in nearest
    assert contact4 not in nearest
    assert contact3 not in nearest
    assert contact2 not in nearest
    assert contact1 not in nearest

