import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
import pytest

from kademlia.RoutingTable import RoutingTable
from kademlia.KBucket import KBucket
from kademlia.Contact import Contact
import kademlia.params as p 

def test_router_get_bucket():
    b = p.params[p.B]
    k = p.params[p.K]
    ip = "127.0.0.1"
    port = 1234

    contact1 = Contact(1, ip, port)
    contact2 = Contact(2, ip, port)
    contact3 = Contact(4, ip, port)
    contact4 = Contact(8, ip, port)

    table = RoutingTable(b, k, 0)

    assert table.add_contact(contact1)
    assert contact1 in table
    assert len(table) == 1
    assert len(table.get_bucket(contact1.getId())) == 1

    assert table.add_contact(contact2)
    assert contact2 in table
    assert len(table) == 2
    assert len(table.get_bucket(contact2.getId())) == 1

    assert table.add_contact(contact3)
    assert contact3 in table
    assert len(table) == 3
    assert len(table.get_bucket(contact3.getId())) == 1

    assert table.add_contact(contact4)
    assert contact4 in table
    assert len(table) == 4
    assert len(table.get_bucket(contact4.getId())) == 1


def test_router_wont_add_self():
    b = p.params[p.B]
    k = p.params[p.K]
    ip = "127.0.0.1"
    port = 1234

    contact = Contact(0, ip, port)
    
    table = RoutingTable(b, k, 0)

    assert not table.add_contact(contact)
    assert contact not in table
    assert len(table) == 0


def test_router_add_contact():
    b = p.params[p.B]
    k = p.params[p.K]
    ip = "127.0.0.1"
    port = 1234

    contact1 = Contact(None, ip, port)
    contact2 = Contact(None, ip, port)
    contact3 = Contact(None, ip, port)
    contact4 = Contact(None, ip, port)

    table = RoutingTable(b, k, 0)

    assert table.add_contact(contact1)
    assert table.add_contact(contact2)
    assert table.add_contact(contact3)
    assert table.add_contact(contact4)

